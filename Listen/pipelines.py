# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.files import FilesPipeline
from urllib.parse import urlparse


class ListenPipeline(FilesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        return '{}/{}/{}'.format(item['web_name'], item['book_name'], item['file_urls'][0].split('/')[-1])  # /ting89/梦里花落知多少/01.mp3'
    def item_completed(self, results, item, info):
        for ok, x in results:
            info.spider.log("下载完成:{}, 文件:{}/{}, 文件url:{}".format(ok, self.store.basedir, x['path'], item['file_urls'][0]))
        return super().item_completed(results, item, info)
