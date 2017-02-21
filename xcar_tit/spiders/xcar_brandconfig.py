# -*- coding: utf-8 -*-

from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from bs4 import BeautifulSoup
import re
import time
import json
from xcar_tit.items import XcarBrandConfigUrlItem
from xcar_tit.Mongodb import monogoservice
from xcar_tit import pipelines


class XcarBrandConfigSpider(RedisSpider):
    name = 'xcar_config'
    api_url = 'http://newcar.xcar.com.cn%s'
    pipeline = set([pipelines.XcarBrandConfigPipeline, ])

    def start_requests(self):
        config_urls = monogoservice.get_config_url()
        for url in config_urls:
            yield Request(self.api_url%url, callback=self.get_url)


    def get_url(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        result = XcarBrandConfigUrlItem()
        url=response.url
        tit=soup.find('title').get_text().strip()
        place=soup.find('div',class_="place")
        if place:
            text=place.get_text().strip()
            add = text.split(':')
            result['address'] = add[1]
        result['category'] = '车系-参数配置'
        result['tit']=tit
        result['url']=url
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