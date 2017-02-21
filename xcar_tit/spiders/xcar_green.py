# -*- coding: utf-8 -*-

from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from bs4 import BeautifulSoup
import re
import time
import json
from xcar_tit.items import XcarGreenItem
from xcar_tit import pipelines

class XcarGreenSpider(RedisSpider):
    name = 'xcar_green'
    api_url='http://green.xcar.com.cn/use/'
    get_url='http://green.xcar.com.cn/green_index.php?d=nev&c=drivecar&page=%d'
    pipeline = set([pipelines.XcarGreenPipeline, ])


    def start_requests(self):
        yield Request(self.api_url,dont_filter=True,callback=self.get_page_list)
        yield Request(self.api_url,callback=self.get_article)


    def get_page_list(self,response):
        page_amount=9
        for page_num in range(1,page_amount+1):
            yield Request(self.get_url%page_num,callback=self.get_list)


    def get_list(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        con_list=soup.find_all('div',class_="leftConSize")
        for con in con_list:
            href=con.find('a').get('href')
            yield Request(href,callback=self.get_article)


    def get_article(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        result = XcarGreenItem()
        url=response.url
        tit=soup.find('title').get_text().strip()
        p1 = soup.find('div',class_="p1")
        if p1:
            text = p1.get_text().strip()
            address = text.split('：')
            result['address'] = address[1]
        result['category'] = '新能源'
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