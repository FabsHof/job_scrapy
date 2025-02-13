# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobScrapyItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    employer = scrapy.Field()
    location = scrapy.Field()