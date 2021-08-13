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

## execute spider

# 配置多个在后续Start的时候会抛异常，所以暂时只能支持单url下载
urls = conf.get('Network', 'urls').split(';')
for url in urls:
    process = CrawlerProcess(project.get_project_settings())
    r1 = process.crawl(ListenSpider, url)
    r2 = process.start()


if conf.getint('Zip', 'enable') == 1:
    setting = project.get_project_settings()
    spider = list(process.spiders._spiders.values())[0]
    file_path = '{}/{}/{}'.format(setting.get('BOOK_FULL_PATH'), spider.name, spider.book_name)
    ## zipfile
    # zipmanager.AddDir(r'E:\Scrapy\Listen\ting89Catch\本次下载的小说的名字')
    zipmanager = ZipManager(prefix='第一序列',sectionsize=conf.getint('Zip','sectionsize'))
    zipmanager.AddDir(setting.get('BOOK_FULL_PATH'))
    zipmanager.ZipAll()
