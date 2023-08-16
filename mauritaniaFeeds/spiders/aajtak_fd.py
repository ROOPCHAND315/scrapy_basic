import scrapy
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(message)s %(filename)s',
                    handlers=[logging.FileHandler("example1.log"),
                              logging.StreamHandler()])
logging.getLogger('scrapy').propagate = False
from ..items import Article

class fullDescriptionclass(scrapy.Spider):
    name = 'aajtak_fd'

    def __init__(self, url=None, *args,**kwargs):
        self.url = url
        super().__init__(url,*args, **kwargs)
    
    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse)

    def parse(self,response):
        logging.info("inside full description")
        item_fd= Article()

        # fd = response.xpath('//div[@class="entry-content entry clearfix"]/p//span/text()').getall()
        fd=''.join(response.xpath('//div[@class="entry-content entry clearfix"]/p/text()').getall())
        item_fd['url'] = self.url
        item_fd['full_description'] =fd
        yield item_fd