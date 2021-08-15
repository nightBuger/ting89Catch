import scrapy
from .items import DmzjItem
import configparser
import re
import logging
import time

class DmzjSpider(scrapy.Spider):

    # start_urls = ['http://www.ting89.com/books/1677.html']


    # 爬虫模块的名字。 根据host解析
    # name = host_url.split('.')[1]   # ting89

    host_url = 'www.dmzj.com'
    name = 'Dmzj' #host_url.split('.')[1]   # ting89

    # 书名。在parse里解析
    book_name = 'book_name'

    def __init__(self, url, *args, **kwargs):
        super(DmzjSpider, self).__init__(*args, **kwargs)
        data = url.split(',')
        self.start_urls = [data[0]]
        self.begin      =  1 if len(data) < 2 else (  1 if data[1]=='' else int(data[1]))
        self.end        = -1 if len(data) < 3 else ( -1 if data[2]=='' else int(data[2]))
        self.log('=============本次爬虫设置: url={}, begin={}, end={}'.format( self.start_urls, self.begin, self.end), logging.INFO)

    def log(self, message, level=logging.INFO, **kw):
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), message)
        super().log(message, level, **kw)
        
    def parse(self,response):
        # 提取书名、作者和简介
        html_desc = response.xpath('//div[@class="comic_deCon"]')
        if len(html_desc) == 0 :
            print (u'\n找不到图书信息，退出!!\n')
            return []
        
        comic_name = html_desc[0].xpath('//h1/a/text()').extract()[0]
        comic_artic = html_desc[0].xpath('//ul[@class="comic_deCon_liO"]/li/text()').extract()[0]
        comic_desc = html_desc[0].xpath('//p[@class="comic_deCon_d"]/text()').extract()[0]
        print (comic_name)
        print (comic_artic)
        print (comic_desc)


        self.book_name = comic_name

        book_list = response.xpath('//div[@class="tab-content zj_list_con autoHeight"]/ul/li/a/@href').getall()
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

        chapter_name = response.xpath('//div[@class="head_title"]/h2/text()')
        if len(chapter_name) == 0:
            self.log('url={}, 无法找到章节信息！！\n status={}, body={}'.format(response.url, response.status, response.text), level=logging.ERROR)
            return []
        else:
            chapter_name = chapter_name.extract()[0]

        # keyword is '91047|3059|jpg|chapterpic|nimg|15197804440344|15197804430503|15197804444439||1519780445l/;3847|u6012|15197804467719|15197804426334|15197804418352|hidden|73154|pages|page_url|img|15197804413517|uff09|chapter_name|230|u7b2c163|u8bdd|u9f99||u9ed1|chapter_order|var|uff08|u4e0a|15197804478109|u7130|sum_pages'
        # pic url is https://images.dmzj.com/img/chapterpic/3059/91047/15197804413517.jpg
        keystring = response.css('head script::text').re("\'\|(.*)\'.split")[0]

        keylist = keystring.split('|')
        keylist = [x for x in keylist if x.isdigit() ]

        key4 = [x for x in keylist if len(x) == 4][0]
        key5 = [x for x in keylist if len(x) == 5][0]
        keypic = [x for x in keylist if len(x) > 10]
        keypic.sort()

        url_list = ['https://images.dmzj.com/img/chapterpic/{}/{}/{}.jpg'.format(key4, key5, x) for x in keypic]

        print(chapter_name)
        print(keystring)
        print(url_list)

        item = DmzjItem()
        item['web_name'] = self.name
        item['book_name'] = self.book_name
        item['ext_name'] = 'jpg'
        item['title'] = chapter_name
        item['image_urls'] = url_list
        yield item

    def parseFinalPage1(self,response):

        chapter_name = response.xpath('//div[@class="head_title"]/h2/text()').extract()[0]

        keyword = response.css('head script::text').re("\'\|(.*)\'.split")[0]
        # keyword is '91047|3059|jpg|chapterpic|nimg|15197804440344|15197804430503|15197804444439||1519780445l/;3847|u6012|15197804467719|15197804426334|15197804418352|hidden|73154|pages|page_url|img|15197804413517|uff09|chapter_name|230|u7b2c163|u8bdd|u9f99||u9ed1|chapter_order|var|uff08|u4e0a|15197804478109|u7130|sum_pages'
        # pic url is https://images.dmzj.com/img/chapterpic/3059/91047/15197804413517.jpg
        pic_list = re.findall('(\d{10,})', keyword)
        pic_list.sort()
        c4 = re.search('(\|\d{4}\|)', keyword).group()[1:-1]  # 3059
        c5 = re.search('(\|\d{5}\|)', keyword).group()[1:-1]  # 91047
        url_list = ['https://images.dmzj.com/img/chapterpic/{}/{}/{}.jpg'.format(c4, c5, x) for x in pic_list]

        # key = keyword.split('|')
        # url_list = ['https://images.dmzj.com/img/{}/{}/{}/{}.{}'.format(key[3], key[1], key[0], x, key[2]) for x in pic_list]


        print(chapter_name)
        print(keyword)
        print(url_list)

        item = DmzjItem()
        item['web_name'] = self.name
        item['book_name'] = self.book_name
        item['ext_name'] = 'jpg'
        item['title'] = chapter_name
        item['image_urls'] = url_list
        yield item
