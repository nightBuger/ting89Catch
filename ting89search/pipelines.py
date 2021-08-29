# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from urllib.parse import urlparse
from scrapy.http import Request
import codecs
from scrapy.utils import project
import time
import sqlite3

class Ting89sPipeline(object):
    conn = sqlite3.connect('test.db')

    def process_item(self, item, spider):

        path = project.get_project_settings().get('FILES_STORE')
        file = codecs.open( '{}/{}.txt'.format(path, item['keyword']), 'a', encoding='utf-8')

        file.writelines(item['result'])
        file.writelines('\n')

        # import sqlite3
        # conn = sqlite3.connect('test.db')
        c = self.conn.cursor()
        sql = 'INSERT INTO `scrapy_result` (keyword, updatetime, result) VALUES ("{}", "{}", "{}");'.format(
            item['keyword'], time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), item['result']
        )
        c.execute(sql)
        self.conn.commit()
        # conn.close()
