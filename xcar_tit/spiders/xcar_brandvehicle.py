# -*- coding: utf-8 -*-

from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from bs4 import BeautifulSoup
import re
import time
import json
from xcar_tit.items import XcarBrandvehicleUrlItem
from xcar_tit.Mongodb import monogoservice
from xcar_tit import pipelines

class XcarBrandvehicleSpider(RedisSpider):
    name = 'xcar_vehicle'
    api_url = 'http://newcar.xcar.com.cn%s'
    pipeline = set([pipelines.XcarBrandVehiclePipeline, ])

    def start_requests(self):
        vehicle_url=monogoservice.get_vehicle_url()
        for url in vehicle_url:
            yield Request(self.api_url%url, callback=self.get_url)


    def get_url(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        result = XcarBrandvehicleUrlItem()
        url=response.url
        tit=soup.find('title').get_text().strip()
        place=soup.find('span',class_="scrap_span")
        if place:
            text=place.get_text().strip()
            result['address'] = text
        result['category'] = '车系-全车详解'
        result['tit']=tit
        result['url']=url
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