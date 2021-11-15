# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class JobparserItem(scrapy.Item):
    _id = scrapy.Field()
    name = scrapy.Field()
    salary = scrapy.Field()
    min_salary = scrapy.Field()
    max_salary = scrapy.Field()
    currency = scrapy.Field()
    url = scrapy.Field()
    site = scrapy.Field()

