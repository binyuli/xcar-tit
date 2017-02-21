# -*- coding: utf-8 -*-

from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from bs4 import BeautifulSoup
import re
import time
import json
from xcar_tit.items import XcarGuideItem
from xcar_tit import pipelines

class XcarGuideSpider(RedisSpider):
    name = 'xcar_guide'
    api_url='http://info.xcar.com.cn/guide/'
    pipeline = set([pipelines.XcarGuidePipeline, ])

    def start_requests(self):
        yield Request(self.api_url,dont_filter=True,callback=self.get_letter)
        yield Request(self.api_url,callback=self.get_article)


    def get_letter(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        li_info=soup.find('div',class_="tnav_style1").find('ul').find_all('li')
        for li in li_info[1:]:
            href=li.find('a').get('href')
            yield Request(href,dont_filter=True,callback=self.get_page_list)
            yield Request(href,callback=self.get_article)

    def get_page_list(self,response):
        url=response.url
        if '239' in url:
            page_amount=69
        elif '811' in url:
            page_amount=68
        elif '243' in url:
            page_amount=37
        elif '245' in url:
            page_amount=30
        else:
            page_amount=58
        for page_num in range(1,page_amount+1):
            page_url=url[:-1]+'_'+str(page_num)+'/'
            yield Request(page_url,callback=self.get_list)

    def get_list(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        li_info=soup.find('div',class_="remark_left").find('ul', class_='leftList').find_all('li',class_="clearfix moreImgSize")
        for li in li_info:
            href=li.find('div',class_="leftConSize").find('a').get('href')
            yield Request(href,callback=self.get_article)

    def get_article(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        result = XcarGuideItem()
        url=response.url
        tit=soup.find('title').get_text().strip()
        p1 = soup.find('div',class_="p1")
        if p1:
            text = p1.get_text().strip()
            address = text.split('：')
            result['address'] = address[1]
        result['category'] = '导购'
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