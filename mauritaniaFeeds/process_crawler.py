from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy import spiderloader
import logging
def feeds():
    process = CrawlerProcess(get_project_settings())
    spider_cls = 'aajtak'
    process.crawl(spider_cls)
    process.start()

feeds()    

def full_description(spider,url):
    
    try:
        project_setting = get_project_settings()
        spider_loader = spiderloader.SpiderLoader.from_settings(project_setting)
        process = CrawlerProcess(get_project_settings())
        # if 'aajtak_fd' in spider_loader.list():
        spider_cls = spider
        logging.info("in full description")
        logging.info(str(url)+"First")
        process.crawl(spider_cls,url=url)
        process.start()
    except Exception as e:
        print("Exception>>>>",str(e))