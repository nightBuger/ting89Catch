import configparser
import os
from Listen.savefile.zipmanager import ZipManager
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings



conf = configparser.ConfigParser()

## init
conf.read(os.path.join(os.path.dirname(os.path.realpath(__file__)),'./config.ini'))
zipmanager = ZipManager(prefix='第一序列',sectionsize=conf.getint('Zip','sectionsize'))

## execute spider
setting = Settings()
print(setting.get('BOT_NAME'))

## zipfile
zipmanager.AddDir('E:\Scrapy\Listen\本次下载的小说的名字')
zipmanager.ZipAll()