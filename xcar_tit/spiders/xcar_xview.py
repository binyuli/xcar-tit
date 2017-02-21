# -*- coding: utf-8 -*-

from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from bs4 import BeautifulSoup
import re
import time
import json
from xcar_tit.items import XcarXviewItem
from xcar_tit import pipelines


class XcarXviewSpider(RedisSpider):
    name = 'xcar_xview'
    get_url='http://info.xcar.com.cn/x-view/'
    pipeline = set([pipelines.XcarViewPipeline, ])

    def start_requests(self):
        yield Request(self.get_url,callback=self.get_letter)


    def get_letter(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        border_info=soup.find_all('div',class_="x_border2")
        for border in border_info:
            href=border.find('div',class_="bg_one1").find('div',class_="onepic").find('a').get('href')
            yield Request(href,callback=self.get_urls)


    def get_urls(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        tit=soup.find('title').get_text().strip()
        url=response.url
        result=XcarXviewItem()
        result['tit'] = tit
        result['url'] = url
        result['category'] = 'X-view'
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