# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from urllib.parse import urlparse
from scrapy.http import Request


class DmzjPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        # for image_url in item['image_urls']:
            # yield Request(image_url)
        return [Request(u) for u in item['image_urls'] ]

    def file_path(self, request, response=None, info=None, *, item=None):
        idx = item['image_urls'].index(request.url) + 1
        return '{}/{}/{}/{:0>3d}.{}'.format(item['web_name'], item['book_name'], item['title'], idx, item['ext_name'])  # /ting89/妖神记/第163话 黑龙怒焰（上）/001.jpg'

    def item_completed(self, results, item, info):
        idx = 0
        for ok, x in results:
            if ok:
                info.spider.log("下载完成: 文件={}/{}, 文件url={}".format(self.store.basedir, x['path'], x['url']))
            else:
                info.spider.log("下载失败：文件url={}".format(item['image_urls'][idx]))
            idx += 1
        return super().item_completed(results, item, info)
