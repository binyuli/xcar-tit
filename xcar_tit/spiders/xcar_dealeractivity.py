# -*- coding: utf-8 -*-

from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from bs4 import BeautifulSoup
import re
import time
import json
from xcar_tit.items import XcarDealerActivityItem
from xcar_tit.Mongodb import monogoservice
from xcar_tit import pipelines


class XcarDealerActivitySpider(RedisSpider):
    name = 'xcar_dealeractivity'
    dealer_url = 'http://dealer.xcar.com.cn%s'
    pipeline = set([pipelines.XcarDealerActivityPipeline, ])

    def start_requests(self):
        activity_url=monogoservice.get_dealeractivity_url()
        for url in activity_url:
            yield Request(self.dealer_url%url,dont_filter=True,callback=self.get_letter)
            yield Request(self.dealer_url%url,callback=self.get_url)


    def get_letter(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        hdlb=soup.find('div',class_="by_detail").find('ul',class_="hdlb")
        if hdlb:
            li_info=hdlb.find_all('li')
            if li_info:
                for li in li_info:
                    href=li.find('div',class_="pic").find('a').get('href')
                    yield Request(self.dealer_url%href,callback=self.get_url)


    def get_url(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        result=XcarDealerActivityItem()
        tit=soup.find('title').get_text().strip()
        url=response.url
        result['tit']=tit
        result['url']=url
        result['category']='经销商-店内活动'
        yield result


    def spider_idle(self):
        """This function is to stop the spider"""
        self.logger.info('the queue is empty, wait for one minute to close the spider')
        time.sleep(60)
        req = self.next_requests()

        if req:
            self.schedule_next_requests()
        else:
            self.crawler.engine.close_spider(self, reason='finished')