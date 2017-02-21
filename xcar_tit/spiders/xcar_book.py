# -*- coding: utf-8 -*-

from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from bs4 import BeautifulSoup
import re
import time
import json
from xcar_tit import pipelines
from xcar_tit.items import XcarBookItem
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

class XcarBookSpider(RedisSpider):
    name = 'xcar_book'
    get_url='http://yp.xcar.com.cn/book/'
    pipeline = set([pipelines.XcarBookPipeline, ])

    def start_requests(self):
        yield Request(self.get_url,dont_filter=True,callback=self.get_letter)
        yield Request(self.get_url,callback=self.get_urls)


    def get_letter(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        banner_cont=soup.find('div',class_="banner_follow").find('div',class_="banner_cont")
        banner_box=banner_cont.find_all('div',class_="banner_box")
        for banner in banner_box:
            li_info=banner.find_all('li')
            for li in li_info:
                href=li.find('a').get('href')
                yield Request(href,dont_filter=True,callback=self.get_page_list)
                yield Request(href,callback=self.get_urls)


    def get_page_list(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        page_info=soup.find('div',id="t_0915_ipage")
        if not page_info:
            page_amount=1
        else:
            info=page_info.find_all('a')
            if len(info)>2:
                m=info[-2].get_text().encode('utf-8')
                page_amount=int(m)
            else:
                page_amount=1
        url=response.url[:-5]
        for page_num in range(1,page_amount+1):
            urls=url+'_'+str(page_num)+'.html'
            yield Request(urls,callback=self.get_list)


    def get_list(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        pag_list=soup.find('div',class_="list_c_lf").find('div',class_="pag_list")
        if pag_list:
            li_info=pag_list.find_all('li')
            for li in li_info:
                href=li.find('div',class_="pag_list_tit").find('p').find('a').get('href')
                yield Request(href,callback=self.get_urls)


    def get_urls(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        tit=soup.find('title').get_text().strip()
        url=response.url
        result=XcarBookItem()
        p1 = soup.find('div',class_="p1")
        if p1:
            text = p1.get_text().strip()
            add = text.split('：')
            result['address'] = add[1][:-2]
        result['tit'] = tit
        result['url'] = url
        result['category'] = '用车宝典'
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

















