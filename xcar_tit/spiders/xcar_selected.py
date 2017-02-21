# -*- coding: utf-8 -*-

from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from bs4 import BeautifulSoup
import re
import time
import json
from xcar_tit.items import XcarSelectedItem
from xcar_tit import pipelines


class XcarSelectedSpider(RedisSpider):
    name = 'xcar_selected'
    get_url='http://club.xcar.com.cn/selected/'
    api_url='http://club.xcar.com.cn%s'
    pipeline = set([pipelines.XcarSelectedPipeline, ])

    def start_requests(self):
        yield Request(self.get_url,dont_filter=True,callback=self.get_letter)
        yield Request(self.get_url,callback=self.get_letter)


    def get_letter(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        sml_title=soup.find('div',id="sml_title").find('div',class_="sort_item item_h35")
        if sml_title:
            a_info=sml_title.find_all('a')
            for info in a_info[1:]:
                href=info.get('href')
                yield Request(self.api_url%href,callback=self.get_page_list)


    def get_page_list(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        page_info=soup.find('div',class_="unify_page")
        if not page_info:
            page_amount=1
        else:
            a_info=page_info.find_all('a')
            if a_info:
                m=a_info[-2].get_text().strip()
                page_amount=int(m)
            else:
                page_amount=1
        url=response.url[:-1]
        for page_num in range(page_amount+1):
            urls=url+'_'+str(page_num)+'/'
            yield Request(urls,callback=self.get_list)

    def get_list(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        guding=soup.find('div',id="guding2")
        if guding:
            li_info=guding.find('ul',class_="sift_ul sift_wrap").find_all('li')
            for li in li_info:
                href=li.find('a').get('href')
                yield Request(href,callback=self.get_urls)


    def get_urls(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        tit=soup.find('title').get_text().strip()
        url=response.url
        result=XcarSelectedItem()
        bread_crumbs = soup.find('div',class_="bread_crumbs")
        if bread_crumbs:
            text = bread_crumbs.get_text().strip()
            add = text.split('：')
            result['address'] = add[1]
        result['tit'] = tit
        result['url'] = url
        result['category'] = '社区精选'
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




















