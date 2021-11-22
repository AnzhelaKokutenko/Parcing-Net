

import scrapy


class InstaparserItem(scrapy.Item):
    _id = scrapy.Field()
    name = scrapy.Field()
    id = scrapy.Field()
    user_id = scrapy.Field()
    user_name = scrapy.Field()
    user_fullname = scrapy.Field()
    photo = scrapy.Field()
    type = scrapy.Field()