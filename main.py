import os
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from src.job_details_pipeline import JobDetailsPipeline
from job_scrapy.spiders.job_spider import JobSpider
from dotenv import load_dotenv

def main():

    query = 'data engineer'
    location = 'ulm'
    diameter = 200

    # process setup
    settings = get_project_settings()
    load_dotenv()

    mongo_user = os.getenv("MONGO_USER")
    mongo_password = os.getenv("MONGO_PASSWORD")
    mongo_db = os.getenv("MONGO_DATABASE")
    mongo_uri = os.getenv("MONGO_URI")

    postgres_host = os.getenv("POSTGRES_HOST")
    postgres_port = os.getenv("POSTGRES_PORT")
    postgres_user = os.getenv("POSTGRES_USER")
    postgres_password = os.getenv("POSTGRES_PASSWORD")
    postgres_db = os.getenv("POSTGRES_DATABASE")

    # ============================
    # ETL pipeline for job search
    # ============================
    # TODO: implement ETL pipeline for job search

    # ============================
    # ELT pipeline for job details
    # ============================
    # crawl job details and store them in MongoDB
    process = CrawlerProcess(settings)
    process.crawl(JobSpider, query=query, location=location, diameter=diameter)
    process.start()

    # transform and load job details from MongoDB to PostgreSQL
    job_details_pipeline = JobDetailsPipeline()
    job_details_pipeline.run(mongo_user, mongo_password, mongo_db, mongo_uri, 'jobs', postgres_host, postgres_port, postgres_user, postgres_password, postgres_db)

if __name__ == "__main__":
    main()
