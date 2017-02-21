# -*- coding: utf-8 -*-

from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from bs4 import BeautifulSoup
import re
import time
import json
from xcar_tit.items import XcarNewCarUrlItem
from xcar_tit import pipelines
from xcar_tit.Mongodb import monogoservice

class XcarNewCarSpider(RedisSpider):
    name = 'xcar_newcar'
    api_url='http://info.xcar.com.cn/'
    article_urls='http://newcar.xcar.com.cn%s'
    pipeline = set([pipelines.XcarNewCarPipeline, ])


    def start_requests(self):
        article_url=monogoservice.get_article_url()
        for url in article_url:
            yield Request(self.article_urls%url, callback=self.get_article)
        yield Request(self.api_url,dont_filter=True,callback=self.get_letter)
        yield Request(self.api_url,callback=self.get_article)


    def get_letter(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        li_info=soup.find('div', class_="tnav_style1").find('ul').find_all('li')
        for li in li_info[2:]:
            href=li.find('a').get('href')
            yield Request(href,dont_filter=True,callback=self.get_types)
            yield Request(href,callback=self.get_article)


    def get_types(self,response):
        url=response.url
        if '650' in url:
            page_amount=3
        elif '362' in url:
            page_amount=45
        elif '562' in url:
            page_amount=7
        elif '848' in url:
            page_amount=27
        elif '214' in url:
            page_amount=1148
        elif '558' in url:
            page_amount=81
        elif '559' in url:
            page_amount=19
        elif '234' in url:
            page_amount=451
        else:
            page_amount=767
        for page_num in range(1,page_amount+1):
            page_url=url[:-1]+'_'+str(page_num)+'/'
            yield Request(page_url,callback=self.get_article_list)


    def get_article_list(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        listCon_title=soup.find_all('dt',class_="listCon_title")
        for listcon in listCon_title:
            href=listcon.find('a').get('href')
            yield Request(href,callback=self.get_article)


    def get_article(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        result = XcarNewCarUrlItem()
        url=response.url
        tit=soup.find('title').get_text().strip()
        current_path=soup.find('div',class_="current_path")
        if current_path:
            p_info=current_path.find('p')
            if p_info:
                text=p_info.get_text().strip()
                add = text.split('：')
                result['address'] = add[1][:-2]

            p1=current_path.find('div',class_="p1")
            if p1:
                text = p1.get_text().strip()
                address = text.split('：')
                result['address'] = address[1]
        place = soup.find('div', class_="place")
        if place:
            text = place.get_text().strip()
            add = text.split(':')
            result['address'] = add[1]
        result['category'] = '新车频道'
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


















