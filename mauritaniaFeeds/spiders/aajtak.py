import scrapy
from ..items import Feeds


class AllfeedsSpider(scrapy.Spider):
    name = 'aajtak'
    
    start_urls = [
        # 'https://www.saharamedias.net/feed/',
        # 'https://elhourriya.net/?feed=rss2',
        # 'http://souhoufi.com/?feed=rss2',
        # 'https://anbaa.info/?feed=rss2',
        'https://khovar.tj/ara/feed/'

    ]


    def parse(self, response):
        response.selector.remove_namespaces()
        allitems= Feeds()
        items = response.xpath("//item")
        for item in items:
            title = item.xpath(".//title/text()").get()
            link = item.xpath(".//link/text()").get()
            description=item.xpath(".//description/text()").get()
            pubDate=item.xpath(".//pubDate/text()").get()

            allitems["title"]=title
            allitems["link"]=link
            allitems["description"]=description
            allitems["pubDate"]=pubDate
            allitems['source_id'] = 'aajtak'

            yield allitems




        
