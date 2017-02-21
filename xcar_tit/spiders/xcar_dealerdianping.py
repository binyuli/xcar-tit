# -*- coding: utf-8 -*-

from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from bs4 import BeautifulSoup
import re
import time
import json
from xcar_tit.items import XcarDealerDianPingItem
from xcar_tit.Mongodb import monogoservice
from xcar_tit import pipelines


class XcarDealerDianPingSpider(RedisSpider):
    name = 'xcar_dealerdianping'
    dealer_url = 'http://dealer.xcar.com.cn%s'
    pipeline = set([pipelines.XcarDealerDianpingPipeline, ])

    def start_requests(self):
        dianping_url=monogoservice.get_dealerdianping_url()
        for url in dianping_url:
            yield Request(self.dealer_url%url,callback=self.get_letter)

    def get_letter(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        result=XcarDealerDianPingItem()
        tit=soup.find('title').get_text().strip()
        url=response.url
        result['tit']=tit
        result['url']=url
        result['category']='经销商-爱卡点评'
        yield result


    def spider_idle(self):
        """This function is to stop the spider"""
        self.logger.info('the queue is empty, wait for one minute to close the spider')
        time.sleep(30)
        req = self.next_requests()

        if req:
            self.schedule_next_requests()
        else:
            self.crawler.engine.close_spider(self, reason='finished')