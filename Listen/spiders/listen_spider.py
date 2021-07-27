import scrapy
from ..items import ListenItem
import configparser

class ListenSpider(scrapy.Spider):
    name = "listen"
    start_urls = [
        # 'http://www.ting89.com/books/15767.html'
        'http://www.ting89.com/books/1677.html'
    ]
    filepath = 'default path'

    def parse(self,response):
        playbook = response.css('div.compress')[0]
        self.filepath = response.css('div.conlist h1::text').get()
        for src in playbook.css('a::attr(href)').getall():
            yield response.follow(src,callback=self.parseFinalPage,encoding='GBK')
    
    def parseFinalPage(self,response):
        audioLink = response.css('head script::text').re_first('var\s+datas=\(\"\S+?\"').split('"')[1].split('&')[0]
        item = ListenItem()
        item['title'] = response.css('div.play_title::text').get()
        item['file_urls'] = [audioLink]
        yield item
