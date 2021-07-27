import configparser
import os
from Listen.savefile.zipmanager import ZipManager
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from scrapy.utils import project
from Listen.spiders.listen_spider import ListenSpider



conf = configparser.ConfigParser()

## init
conf.read(os.path.join(os.path.dirname(os.path.realpath(__file__)),'./config.ini'))
zipmanager = ZipManager(prefix='第一序列',sectionsize=conf.getint('Zip','sectionsize'))

## execute spider
setting = project.get_project_settings()
process = CrawlerProcess(project.get_project_settings())

process.crawl(ListenSpider)
process.start()


## zipfile
zipmanager.AddDir(r'E:\Scrapy\Listen\ting89Catch\本次下载的小说的名字')
zipmanager.ZipAll()