# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Ting89sItem(scrapy.Item):
    keyword = scrapy.Field()
    result = scrapy.Field()
