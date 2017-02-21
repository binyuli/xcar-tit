# -*- coding: utf-8 -*-

from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from bs4 import BeautifulSoup
from xcar_tit.items import XcarUsedCarItem
import math
import time
import json
import sys
from xcar_tit import pipelines


class XcarUsedcarSpider(RedisSpider):
    name = 'xcar_usedcar'
    get_url = 'http://used.xcar.com.cn/search/'
    api_url='http://used.xcar.com.cn%s'
    pipeline = set([pipelines.XcarUsedCarPipeline, ])


    def start_requests(self):
        yield Request(self.get_url,callback=self.get_letter)


    def get_letter(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        pbid_ul=soup.find('div',class_="option_wrap option_divs clearfix").find('div',class_="option").find('ul',class_="pbid_ul")
        li_info=pbid_ul.find_all('li')
        for li in li_info[1:]:
            href=li.find('a').get('href')
            yield Request(self.api_url%href,callback=self.get_vehicle)


    def get_vehicle(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        pserid_ul=soup.find('div',class_="option_wrap clearfix").find('div',class_="option").find('ul',class_="pserid_ul")
        li_info=pserid_ul.find_all('li')
        for li in li_info[1:]:
            cid=li.get('value')
            if '#' in cid:
                continue
            href=li.find('a').get('href')
            yield Request(self.api_url%href,callback=self.get_page_usedcar)


    def get_page_usedcar(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        count=soup.find('div',class_="newcar_top").find('span',class_="car_source").find('b').get_text()
        if int(count)!=0:
            num=math.ceil(float(count)/40)
            page_amount=int(num)
            for page_num in range(1,page_amount+1):
                url='%s?page=%d'%(response.url,page_num)
                yield Request(url,callback=self.get_usedcar_list)


    def get_usedcar_list(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        ul_info=soup.find('ul',class_="cal_ul clearfix")
        if ul_info:
            li_info=ul_info.find_all('li',class_="li_hover")
            for li in li_info:
                href=li.find('div',class_="cal_main").find('p',class_="cal_main_title").find('a').get('href')
                style=li.find('div',class_="cal_main").find('p',class_="cal_main_title").find('a').get('title')
                yield Request(self.api_url%href,callback=self.get_usedcar)


    def get_usedcar(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        result = XcarUsedCarItem()
        url = response.url
        tit = soup.find('title').get_text().strip()
        place = soup.find('div', class_="place")
        if place:
            text = place.get_text().strip()
            add = text.split(':')
            result['address'] = add[1]
        result['category'] = '车系-二手车'
        result['tit'] = tit
        result['url'] = url
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

