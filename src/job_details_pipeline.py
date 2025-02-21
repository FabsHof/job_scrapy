import pandas as pd
from pymongo import MongoClient
import psycopg
import logging

class JobDetailsPipeline(object):
    """
    Singleton class to process job details and store them in a database.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(JobDetailsPipeline, cls).__new__(cls)
            cls._instance.logger = logging.getLogger(cls.__name__)
        return cls._instance
        
    def _init_mongo_connection(self, mongo_user: str, mongo_password: str, mongo_db: str, mongo_uri: str, collection_name: str) -> None:
        self.logger.info('>> Initializing MongoDB connection...')
        self.mongo_client = MongoClient(mongo_uri % (mongo_user, mongo_password))
        self.mongo_db = self.mongo_client[mongo_db]
        self.mongo_collection = self.mongo_db[collection_name]
        self.logger.info('>> MongoDB connection initialized!')

    def run(self, mongo_user: str = None, mongo_password: str = None, mongo_db: str = None, mongo_uri: str = None, collection_name: str = None, 
            postgres_host: str = None, postgres_port: int = None, postgres_user: str = None, postgres_password: str = None, postgres_db: str = None) -> None:
        self._init_mongo_connection(mongo_user, mongo_password, mongo_db, mongo_uri, collection_name)

        # Fetch and process data
        self.logger.info('>> Fetching data from MongoDB...')
        mongo_data = list(self.mongo_collection.find())
        self.logger.info('>> Fetched %s records from MongoDB', len(mongo_data))
        df = pd.DataFrame(mongo_data)

        # Clean data by dropping unnecessary columns and duplicates.
        self.logger.info('>> Processing data...')
        df_processed = df.drop(columns=['_id', 'title', 'employer', 'location'])
        df_processed['job_id'] = df_processed['url'] \
            .apply(lambda url: url.split('/')[-1]) \
            .apply(lambda url: url.split('?')[0])
        df_processed.drop_duplicates(subset=['job_id'], inplace=True)
        df_processed['detail_url'] = df_processed['url']
        df_processed = df_processed.drop(columns=['url'])
        self.logger.info('>> Processed data columns: %s', df_processed.columns)

        # PostgreSQL connection
        with psycopg.connect(
            host=postgres_host,
            port=postgres_port,
            dbname=postgres_db,
            user=postgres_user,
            password=postgres_password
        ) as connection:
            with connection.cursor() as cursor:
                self.logger.info('>> Storing data in PostgreSQL...')
                for row in df_processed.iterrows():
                    data = row[1]
                    # Create a tuple for correct mapping of search_params to the custom type in PostgreSQL
                    search_params_value = (
                        data['search_params']['query'],
                        data['search_params']['location'],
                        data['search_params']['diameter']
                    )
                    try :
                        cursor.execute('''
                            INSERT INTO JobDetails (job_id, details_url, search_params)
                            VALUES (%s, %s, %s)
                        ''', (data['job_id'], data['detail_url'], search_params_value))
                    except psycopg.errors.UniqueViolation:
                        self.logger.warning(f'Job with id {data["job_id"]} already exists in the database.')
                    except Exception as e:
                        self.logger.error('Error inserting data into PostgreSQL: %s', e)
                self.logger.info('>> Data stored in PostgreSQL!')
                connection.commit()
        
        self.logger.info('>> Job details pipeline completed!')

