# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.files import FilesPipeline
from urllib.parse import urlparse


class ListenPipeline(FilesPipeline):
    # def process_item(self, item, spider):
    #     return item
    # def file_path(self, request, response=None, info=None, *, item=None):
    #     print(response.body)
    #     return super().file_path(request, response=response, info=info, item=item)
    def file_path(self, request, response=None, info=None, *, item=None):
        return self.pathname + item['title'] + '.mp3'
    def open_spider(self, spider):
        self.pathname = '/本次下载的小说的名字/'
        return super().open_spider(spider)
    