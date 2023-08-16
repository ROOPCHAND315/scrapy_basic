import sys_path
import CentralSpider
from datetime import datetime
from DateTime import DateTime
from w3lib.html import remove_tags
import hashlib
import logging

class Electrek_24(CentralSpider.CentralSpider):
    name = '24electrek'

    def parse(self, response):
        try:
            self.response_log(status_response=response.status)
            cur_time=datetime.utcnow().replace(microsecond=0)
            if response.status !=200:
                log = self.exception_log(status_response=response.status, cur_time=cur_time)
                self.failed_spider(spider_name=self.name,error_code=response.status,cur_time=cur_time)
                yield log
            else:
                def crawl_feeds(item):
                    feed = dict()
                    try:
                        feed['title']=' '.join(item.xpath('title/text()').extract()[0].split())
                    except:
                        feed['title']=None
                    try:
                        feed['link']=' '.join(item.xpath('link/text()').extract()[0].split())
                        feed['link_hash']=hashlib.md5((feed['link']).encode()).hexdigest()
                    except:
                        feed['link']=None
                    try:
                        feed['creator']=item.xpath('*[local-name()="creator" and namespace-uri()="http://purl.org/dc/elements/1.1/"]/text()').extract()
                    except:
                        feed['creator'] = None
                    try:
                        feed['keywords']=item.xpath('category/text()').extract()
                    except:
                        feed['keywords'] = None
                    try:
                        description= remove_tags(item.xpath('description/text()').extract()[0])
                        feed['description'] = ' '.join(description.split())
                    except:
                        feed['description']=None
                    try:
                        content = remove_tags(item.xpath('*[local-name()="encoded" and namespace-uri()="http://purl.org/rss/1.0/modules/content/"]/text()').extract()[0])
                        feed['content'] = ' '.join(content.split())
                    except:
                        feed['content']=None
                    try:
                        feed['media']=item.xpath('*/@url').extract()[0]
                    except:
                        feed['media'] = None
                    datetime_obj=DateTime()
                    try:
                        value,code=datetime_obj.get_datetime(date=' '.join(item.xpath('pubDate/text()').extract()[0].split()))
                        if code==200:
                            feed['pubDate']=value
                        else:
                            feed['pubDate']=None
                            self.failed_spider(spider_name=self.name,reason=value,cur_time=cur_time)
                    except:
                        pass
                    feed['updated_at'] = datetime.utcnow().replace(microsecond=0).strftime('%Y-%m-%d %H:%M:%S')
                    return feed
                items = response.xpath('//channel/item')
                for item in items:
                    feed_items = crawl_feeds(item)
                    if (feed_items['title'] is not None) and (feed_items['link'] is not None) and (feed_items['pubDate'] is not None):
                        news_items = self.save_data(title=feed_items['title'],link=feed_items['link'],link_hash=feed_items['link_hash'],keywords=feed_items['keywords'],
                                creator=feed_items['creator'],description=feed_items['description'],content=feed_items['content'],media = feed_items['media'],
                                pubDate=feed_items['pubDate'],created_at=cur_time, updated_at=feed_items['updated_at'])
                        if(self.link_id.check_insert):
                            yield news_items
                        else:
                            break
                    else:
                        pass
        except Exception as e:
            self.failed_spider(spider_name=self.name,reason=str(e),cur_time=cur_time)
            logging.error(str(e))