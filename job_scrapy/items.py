# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobScrapyItem(scrapy.Item):
    _id = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    employer = scrapy.Field()
    location = scrapy.Field()
    search_params = scrapy.Field()