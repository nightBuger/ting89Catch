# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DmzjItem(scrapy.Item):
    web_name = scrapy.Field()
    book_name = scrapy.Field()
    ext_name = scrapy.Field()
    title = scrapy.Field()
    image_urls = scrapy.Field()
