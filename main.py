from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from job_scrapy.spiders.job_spider import JobSpider
import os
from dotenv import load_dotenv

def main():
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

    process = CrawlerProcess(settings)
    process.crawl(JobSpider, query="data engineer", location="ulm")
    process.start()


if __name__ == "__main__":
    main()
