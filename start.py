import configparser
import os
from Listen.savefile.zipmanager import ZipManager
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from scrapy.utils import project
from Listen.spiders.listen_spider import ListenSpider
from Dmzj.dmzj_spider import DmzjSpider
from ting89search.ting89s_spider import Ting89sSpider
import re

def GetSpiderList(cfgname):
    conf = configparser.ConfigParser()
    conf.read(os.path.join(os.path.dirname(os.path.realpath(__file__)), cfgname))
    spider_path = conf.items('settings')
    spider_module = [x[0] for x in spider_path]
    return spider_module

    # 本想从spider中获取name，结果遍历失败
    from scrapy.utils.misc import walk_modules
    from scrapy.utils.spider import iter_spider_classes

    spider_name = []
    for module in spider_module:
        for module1 in walk_modules(module):
            for spcls in iter_spider_classes(module1):
                spider_name.append(spcls.name)
    return spider_name



def main():
    spider_factory = GetSpiderList('scrapy.cfg')

    ## init
    conf = configparser.ConfigParser()
    conf.read(os.path.join(os.path.dirname(os.path.realpath(__file__)),'./config.ini'), encoding='utf-8')

    # 通过url，解析爬虫名字 ( 取 //和/之间的域名，用'.'分割，之后取倒数第二个作为爬虫名字)
    url = conf.get('Network', 'url')
    spider_name = re.search('\/\/.*?\/', url).group().split('.')[-2]
    if spider_name not in spider_factory:
        print("url not support!!!", url)
        exit(0)

    os.environ['SCRAPY_PROJECT'] = spider_name
    setting = project.get_project_settings()
    process = CrawlerProcess(setting)
    r1 = process.crawl(spider_name, url)
    r2 = process.start()


	# if conf.getint('Zip', 'enable') == 1:
	#     setting = project.get_project_settings()
	#     spider = list(process.spiders._spiders.values())[0]
	#     file_path = '{}/{}/{}'.format(setting.get('BOOK_FULL_PATH'), spider.name, spider.book_name)
	#     ## zipfile
	#     # zipmanager.AddDir(r'E:\Scrapy\Listen\ting89Catch\本次下载的小说的名字')
	#     zipmanager = ZipManager(prefix='第一序列',sectionsize=conf.getint('Zip','sectionsize'))
	#     zipmanager.AddDir(setting.get('BOOK_FULL_PATH'))
	#     zipmanager.ZipAll()

if __name__ == "__main__":
	main()
