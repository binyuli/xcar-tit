# -*- coding: utf-8 -*-

from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from bs4 import BeautifulSoup
import re
import time
import json
from xcar_tit.items import XcarSUVItem
from xcar_tit import pipelines

class XcarSUVSpider(RedisSpider):
    name = 'xcar_suv'
    api_url='http://suv.xcar.com.cn/'
    pipeline = set([pipelines.XcarSuvPipeline, ])

    def start_requests(self):
        yield Request(self.api_url,callback=self.get_letter)


    def get_letter(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        li_info=soup.find('div',class_="tnav_style1").find('ul').find_all('li')
        for li in li_info[2:5]:
            href=li.find('a').get('href')
            yield Request(href,callback=self.get_types)
        url=li_info[6].find('a').get('href')
        yield Request(url, callback=self.get_type)


    def get_type(self,response):
        page_amount=2
        url = response.url
        urls=url.split('.htm')
        for page_num in range(1,page_amount+1):
            page_url=urls[0]+'_'+str(page_num)+'.html'
            yield Request(page_url,callback=self.get_article_lists)


    def get_types(self,response):
        url=response.url
        if 'news' in url:
            page_amount=40
        elif 'guide' in url:
            page_amount=13
        else :
            page_amount=8
        for page_num in range(1,page_amount+1):
            page_url=url[:-1]+'_'+str(page_num)+'/'
            yield Request(page_url,callback=self.get_article_list)


    def get_article_lists(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        pag_list_tit = soup.find_all('div',class_="pag_list_tit")
        for pag in pag_list_tit:
            href = pag.find('p').find('a').get('href')
            yield Request(href, callback=self.get_article)


    def get_article_list(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        listCon_title = soup.find_all('dt', class_="listCon_title")
        for listcon in listCon_title:
            href = listcon.find('a').get('href')
            yield Request(href, callback=self.get_article)


    def get_article(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        result = XcarSUVItem()
        url=response.url
        tit=soup.find('title').get_text().strip()
        current_path = soup.find('div', class_="current_path")
        if current_path:
            p_info = current_path.find('p')
            if p_info:
                text = p_info.get_text().strip()
                add = text.split('：')
                result['address'] = add[1][:-2]

            p1 = current_path.find('div', class_="p1")
            if p1:
                text = p1.get_text().strip()
                address = text.split('：')
                result['address'] = address[1]
        result['category'] = 'SUV'
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











