import scrapy
from .items import Ting89sItem
import configparser
import re
import logging
import time
import json
import urllib.parse as parse

class Ting89sSpider(scrapy.Spider):

    host_url = 'www.ting89.com'
    name ='ting89s'

    def __init__(self, url, *args, **kwargs):
        super(Ting89sSpider, self).__init__(*args, **kwargs)
        self.keyword = url.split('/')[-1]
        keyword = parse.quote(self.keyword, encoding='gbk')
        url = r"http://www.ting89.com/search.asp?searchword={}&searchtype=-1&submit=%CB%D1%CB%F7".format(keyword)
        self.start_urls = [url]


    def log(self, message, level=logging.INFO, **kw):
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), message)
        super().log(message, level, **kw)
        
    def parse(self,response):

        lstObj = response.xpath('//div[@class="clist"]/ul/li')
        for node in lstObj:
            print(node)
            name =  node.xpath('a/@title').extract()[0]
            url  = node.xpath('a/@href').extract()[0]
            desc = node.xpath('p/text()').extract()[:-1]
            desc.insert(0, '书名：'+ name)
            desc.append(self.host_url + url)

            item = Ting89sItem()
            item['keyword'] = self.keyword
            item['result'] = ', '.join(desc)
            print(item)
            yield item
