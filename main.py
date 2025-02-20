from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from job_scrapy.spiders.job_spider import JobSpider
import os
from dotenv import load_dotenv

def main():

    query = 'data engineer'
    location = 'ulm'
    diameter = 200

    # process setup
    settings = get_project_settings()
    load_dotenv()

    feed_uri = os.getenv("FEED_URI", "data/jobs.json")
    feed_format = os.getenv("FEED_FORMAT", "json")
    feed_overwrite = os.getenv("FEED_OVERWRITE", "True").lower() in ("true", "1", "t")

    settings.set("FEEDS", {
        feed_uri: {
            "format": feed_format,
            "overwrite": feed_overwrite,
        },
    })

    # ELT pipeline for job details
    process = CrawlerProcess(settings)
    process.crawl(JobSpider, query=query, location=location, diameter=diameter)
    process.start()

    # TODO: Call job_details_pipeline to transform the job details and load them into the database



    # TODO: Create an API call to get the data from the feed_uri


if __name__ == "__main__":
    main()
