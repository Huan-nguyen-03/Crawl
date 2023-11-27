# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HrefItem(scrapy.Item):
    # define the fields for your item here like:
    
    type = scrapy.Field()
    id = scrapy.Field()
    name = scrapy.Field()
    # issuance_time = scrapy.Field()
    # effective_time = scrapy.Field()
    # note = scrapy.Field()

    href = scrapy.Field()
    title = scrapy.Field()
    pass

class HrefItemKHCN(scrapy.Item):
    # define the fields for your item here like:
    
    i = scrapy.Field()
    href = scrapy.Field()
    title = scrapy.Field()

class LawItem(scrapy.Item):
    # define the fields for your item here like:
    type = scrapy.Field()
    id = scrapy.Field()
    href = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    pass


class LawItemKHCN(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    href = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    pass