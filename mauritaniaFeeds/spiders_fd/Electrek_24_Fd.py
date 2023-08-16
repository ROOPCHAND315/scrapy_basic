import sys_path
import CentralSpider
from datetime import datetime
import logging

class Electrek_24_Fd(CentralSpider.CentralSpider_Fd):
    name = '24electrek_fd'

    def parse(self, response):
        try:
            self.response_log(status_response=response.status)
            cur_time=datetime.utcnow().replace(microsecond=0)
            if response.status !=200:
                log = self.exception_log(status_response=response.status, cur_time=cur_time)           # Calling exception_log method in Base
                self.failed_domain(spider_name=self.name,error_code=response.status,cur_time=cur_time)
                if response.status != 404:
                    news_items = self.save_full_description(full_description_status=0)
                yield log
            if response.status == 404:
                news_items = self.save_full_description(full_description_status=2)
            elif response.status == 200:
                full_description=' '.join(' '.join(response.xpath("//div[@id='content']//p[not(self::script)]/text()[not(ancestor::*[self::style])]").extract()).split())
                if len(full_description) !=0:
                    news_items=self.save_full_description(full_description=full_description,full_description_status=1)
                else:
                    news_items=self.save_full_description(full_description_status=0)
                    self.failed_domain(spider_name=self.name,reason="xpath has been changed or has no content",cur_time=cur_time)
            yield news_items
        except Exception as e:
            self.failed_domain(spider_name=self.name,reason=str(e),cur_time=cur_time)
            logging.error(str(e))

    def failed_response(self,reponse):
        news_items=self.save_full_description(full_description_status=0)
        self.failed_domain(spider_name=self.name,reason="DNS lookup failed or has reached max redirections",cur_time=datetime.utcnow().replace(microsecond=0))
        yield news_items