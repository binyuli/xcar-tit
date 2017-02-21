# -*- coding: utf-8 -*-

from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from bs4 import BeautifulSoup
import re
import time
import json
from xcar_tit.items import XcarDealerCarPriceItem
from xcar_tit import pipelines


class XcarDealerCarPriceSpider(RedisSpider):
    name = 'xcar_carprice'
    get_url='http://price.xcar.com.cn/city9999-0-1.htm'
    api_url='http://price.xcar.com.cn%s'
    pipeline = set([pipelines.XcarCarPricePipeline, ])

    def start_requests(self):
        yield Request(self.get_url,dont_filter=True,callback=self.get_letter)
        yield Request(self.get_url,callback=self.get_urls)

    def get_letter(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        fra_box_lt=soup.find('div',class_="fra_box_lt")
        if fra_box_lt:
            li_info=fra_box_lt.find('ul',id="menu_ul").find_all('li',menu=True)
            for li in li_info:
                infos=li.find('a')
                if infos:
                    href=infos.get('href')
                    yield Request(self.api_url%href,dont_filter=True,callback=self.get_car_list)
                    yield Request(self.api_url%href,callback=self.get_urls)


    def get_car_list(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        pr_info=soup.find_all('div',class_="pr_rp1")
        for pr in pr_info:
            li_info=pr.find('ul').find_all('li')
            for li in li_info:
                href=li.find('a').get('href')
                yield Request(self.api_url%href,dont_filter=True,callback=self.get_list)
                yield Request(self.api_url%href,callback=self.get_urls)


    def get_list(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        t_wti=soup.find('div',class_="t_wti_0915_taba")
        if t_wti:
            tbody=t_wti.find('table',border="0").find('tbody')
            if tbody:
                tr_info=tbody.find_all('tr')
                for tr in tr_info:
                    f_eclip=tr.find('td',class_="f_eclip t1126_ahau")
                    if f_eclip:
                        href=f_eclip.find('a').get('href')
                        yield Request(self.api_url%href,callback=self.get_urls)


    def get_urls(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        result=XcarDealerCarPriceItem()
        tit=soup.find('title').get_text().strip()
        url=response.url
        crumbs=soup.find('div',class_="crumbs")
        if crumbs:
            text=crumbs.get_text().strip()
            add = text.split('：')
            result['address'] = add[1]
        result['tit']=tit
        result['url']=url
        result['category']='汽车报价'
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











