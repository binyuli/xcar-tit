# -*- coding: utf-8 -*-

from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from bs4 import BeautifulSoup
import re
import time
import json
from xcar_tit.items import XcarDriveItem
from xcar_tit import pipelines

class XcarDriveSpider(RedisSpider):
    name = 'xcar_drive'
    api_url='http://drive.xcar.com.cn/'
    pipeline = set([pipelines.XcarDrivePipeline, ])

    def start_requests(self):
        yield Request(self.api_url,dont_filter=True,callback=self.get_letter)
        yield Request(self.api_url,callback=self.get_article)

    def get_letter(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        li_info=soup.find('div',class_="tnav_style1").find_all('li')
        for li in li_info[1:4]:
            href=li.find('a').get('href')
            yield Request(href,dont_filter=True,callback=self.get_types)
            yield Request(href,callback=self.get_types)
        urls=li_info[4].find('a').get('href')
        yield Request(urls,dont_filter=True,callback=self.get_travle)
        yield Request(urls,callback=self.get_article)

    def get_travle(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        page_info=soup.find('p',class_='article_page_bottom').find_all('a',class_="page")
        page_amount=page_info[-1].get_text().strip()
        for page_num in range(1,int(page_amount)+1):
            url='%s?&m=go&page=%d#xcar_travel'%(response.url,page_num)
            yield Request(url,callback=self.get_page_list)

    def get_page_list(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        li_info = soup.find('ul', id="travel_list").find_all('li')
        for li in li_info:
            href=li.find('dl').find('dt').find('a').get('href')
            yield Request(href,callback=self.get_article)

    def get_types(self,response):
        url=response.url
        if '833' in url:
            page_amount=6
        elif '120' in url:
            page_amount=90
        else:
            page_amount=29
        for page_num in range(page_amount+1):
            page_url=url[:-1]+'_'+str(page_num)+'/'
            yield Request(page_url,callback=self.get_list)

    def get_list(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        li_info = soup.find('div', class_="remark_left").find('ul', class_='leftList').find_all('li',class_="clearfix moreImgSize")
        for li in li_info:
            href = li.find('div', class_="leftConSize").find('a').get('href')
            yield Request(href, callback=self.get_article)

    def get_article(self, response):
        soup = BeautifulSoup(response.body_as_unicode())
        result = XcarDriveItem()
        url = response.url
        tit = soup.find('title').get_text().strip()
        p1 = soup.find('div', class_="p1")
        if p1:
            text = p1.get_text().strip()
            address = text.split('：')
            result['address'] = address[1]
        result['category'] = '试驾'
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