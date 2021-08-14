import scrapy
from ..items import ListenItem
import configparser
import re
import logging
import time

class ListenSpider(scrapy.Spider):

    # start_urls = ['http://www.ting89.com/books/1677.html']

    # 网站的host。根据 start_urls解析    # www.ting89.com
    # host_url = re.search('www.*com', start_urls[0])
    # host_url = host_url.group() if host_url else '' 

    # 爬虫模块的名字。 根据host解析
    # name = host_url.split('.')[1]   # ting89

    host_url = 'http://www.ting89.com/'
    name = host_url.split('.')[1]   # ting89

    # 书名。在parse里解析
    book_name = 'book_name'

    def __init__(self, url, *args, **kwargs):
        super(ListenSpider, self).__init__(*args, **kwargs)
        data = url.split(',')
        self.start_urls = [data[0]]
        self.begin      =  1 if len(data) < 2 else (  1 if data[1]=='' else int(data[1]))
        self.end        = -1 if len(data) < 3 else ( -1 if data[2]=='' else int(data[2]))
        self.log('=============本次爬虫设置: url={}, begin={}, end={}'.format( self.start_urls, self.begin, self.end), logging.INFO)

    def log(self, message, level=logging.INFO, **kw):
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), message)
        super().log(message, level, **kw)
        
    def parse(self,response):
        # self.book_name = response.xpath('//div[@class="conlist"]')[0].xpath('//h1/text()').extract()[0]
        self.book_name = response.css('div.conlist h1::text').get()

        playbook    = response.css('div.compress')[0]
        book_list    = playbook.css('a::attr(href)').getall()
        self.begin  = min(self.begin, len(book_list))
        self.end    = min(self.end, len(book_list))
        book_list = book_list[self.begin-1 : self.end]
        self.log('=============爬虫实际抓取: 书名={}, 起始章节={}, 结束章节={}, 共{}章'.format( self.book_name, self.begin, self.end, len(book_list)) )

        # 因为实际下载时，总是逆序下载（除了第一个章节），为了美观，我们先翻转一下下载顺序
        true_list = list(reversed(book_list[1:]))
        true_list.insert(0, book_list[0])
        for src in true_list:
            # self.log('=============本次爬虫实际抓取地址为 {}'.format( src) )
            yield response.follow(src,callback=self.parseFinalPage,encoding='GBK')
    
    def parseFinalPage(self,response):
        audioLink = response.css('head script::text').re_first('var\s+datas=\(\"\S+?\"').split('"')[1].split('&')[0]
        item = ListenItem()
        item['web_name'] = self.name
        item['book_name'] = self.book_name
        item['title'] = response.css('div.play_title::text').get()
        item['file_urls'] = [audioLink]
        yield item
