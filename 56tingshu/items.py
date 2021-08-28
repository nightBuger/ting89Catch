# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ListenItem(scrapy.Item):
    web_name = scrapy.Field()
    book_name = scrapy.Field()
    index = scrapy.Field()
    title = scrapy.Field()
    file_urls = scrapy.Field()
