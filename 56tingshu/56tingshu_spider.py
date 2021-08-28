import scrapy
from .items import ListenItem
import re
import logging
import time
import urllib

class TingshuSpider(scrapy.Spider):

    host_url = 'https://www.56tingshu.com/'
    name = host_url.split('.')[1]   # ting89

    # 书名。在parse里解析
    book_name = 'book_name'

    def __init__(self, url, *args, **kwargs):
        super(TingshuSpider, self).__init__(*args, **kwargs)
        data = url.split(',')
        self.start_urls = [data[0]]
        self.begin      = 1 if len(data) < 2 else ( 1 if data[1]=='' else int(data[1]))
        self.end        = 0 if len(data) < 3 else ( 0 if data[2]=='' else int(data[2]))
        self.log('=============本次爬虫设置: url={}, begin={}, end={}'.format( self.start_urls, self.begin, self.end), logging.INFO)

    def log(self, message, level=logging.INFO, **kw):
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), message)
        super().log(message, level, **kw)
        
    def parse(self,response):
        # self.book_name = response.xpath('//div[@class="conlist"]')[0].xpath('//h1/text()').extract()[0]
        html_desc = response.xpath('//div[@class="conlist"]')
        if len(html_desc) == 0:
            self.log('无法找到描述信息部分(div=conlist), 退出!!', level=logging.ERROR)
            return []
        
        html_title = html_desc[0].xpath('ul/li/center/h1/text()')
        if len(html_title) == 0:
            self.log('无法找到标题(ul/li/center/h1/text()), 退出!!', level=logging.ERROR)
            return []
                   
        self.book_name = html_title.extract()[0]

        book_list   = response.xpath('//ul[@class="compress"]/li')
        self.begin  = min(self.begin, len(book_list))
        self.end    = len(book_list) if self.end <= 0 else min(self.end, len(book_list))
        temp_list   = book_list[self.begin-1 : self.end]
        self.log('=============爬虫实际抓取: 书名={}, 共{}章; 抓取起始章节={}, 结束章节={}, 抓取{}章'.format( self.book_name, len(book_list), self.begin, self.end, len(temp_list)) )

        # 因为实际下载时，总是逆序下载（除了第一个章节），为了美观，我们先翻转一下下载顺序
        true_list = list(reversed(temp_list[1:]))
        true_list.insert(0, temp_list[0])
        for one in true_list:
            # one is '<li><a title="第0001集" href="/play/15-0-0.html" target="_blank">第0001集</a></li>'
            item = ListenItem()
            item['web_name'] = self.name
            item['book_name'] = self.book_name
            item['title'] = one.xpath('a/text()').extract()[0]
            yield response.follow(one.xpath('a/@href')[0], callback=self.parseFinalPage,encoding='GBK', cb_kwargs=dict(item=item))
    
    def parseFinalPage(self,response, item):
        self.host_url = 'http://wting.info'
        script = response.xpath('//div[@class="border"]/script')[0].extract()
        audio_url = re.search('http.*?"\)', script).group()[:-2]
        audio_url = urllib.parse.unquote(audio_url)
        item['file_urls'] = [audio_url]
        yield item
