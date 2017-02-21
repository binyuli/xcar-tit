# -*- coding: utf-8 -*-

from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from bs4 import BeautifulSoup
from xcar_tit.items import XcarIndexUrlItem
import time
import re
from xcar_tit import pipelines

class XcarIndexSpider(RedisSpider):
    name = 'xcar_index'
    url='http://www.xcar.com.cn/'
    pipeline = set([pipelines.XcarIndexPipeline, ])

    def start_requests(self):
        yield Request(self.url,callback=self.get_letter)


    def get_letter(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        ul_info=soup.find('div',class_="nav").find_all('ul')
        for ul in ul_info:
            li_info=ul.find_all('li')
            for li in li_info:
                href=li.find('a').get('href')
                yield Request(href,callback=self.get_url)
        div_info=soup.find('div',class_="nc_width").find_all('a')
        for div in div_info:
            url=div.get('href')
            yield Request(url,callback=self.get_url)
        top_info=soup.find('div',class_="nc_top").find_all('a')
        for top in top_info:
            urls=top.get('href')
            yield Request(urls,callback=self.get_url)


    def get_url(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        result=XcarIndexUrlItem()
        url=response.url
        tit=soup.find('title').get_text().strip()
        result['title']=tit
        result['url']=url
        yield result


    def spider_idle(self):
        """This function is to stop the spider"""
        req = self.next_requests()
        if req:
            self.schedule_next_requests()
        else:
            self.crawler.engine.close_spider(self, reason='finished')