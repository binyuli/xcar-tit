# -*- coding: utf-8 -*-

from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from bs4 import BeautifulSoup
import re
import time
import json
from xcar_tit.items import XcarDealerPriceItem
from xcar_tit.Mongodb import monogoservice
from xcar_tit import pipelines

class XcarDealerPriceSpider(RedisSpider):
    name = 'xcar_dealerprice'
    dealer_url='http://dealer.xcar.com.cn%s'
    pipeline = set([pipelines.XcarDealerPricePipeline, ])

    def start_requests(self):
        price_url=monogoservice.get_dealerprice_url()
        for url in price_url:
            yield Request(self.dealer_url%url,dont_filter=True,callback=self.get_letter)
            yield Request(self.dealer_url%url,callback=self.get_dealer_url)


    def get_letter(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        f1=soup.find('div',class_="f1")
        if f1:
            jxs_zypp=f1.find('div',class_="jxs_zypp").find('div',class_="n")
            ul_info=jxs_zypp.find_all('ul',class_="jxs_l3")
            for ul in ul_info:
                li_info=ul.find_all('li')
                for li in li_info[2:]:
                    href=li.find('a').get('href')
                    yield Request(self.dealer_url%href,dont_filter=True,callback=self.get_page_list)
                    yield Request(self.dealer_url%href,callback=self.get_dealer_url)


    def get_page_list(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        page_info=soup.find('p',class_="t_0915_ipage")
        if not page_info:
            page_amount=1
        else:
            a_info=page_info.find_all('a')
            m=a_info[-2].get_text().strip()
            if m:
                page_amount=int(m)
            else:
                page_amount=1
        for page_num in range(page_amount+1):
            url=response.url[:-5]+str(page_num)+'.htm'
            yield Request(url,callback=self.get_list)


    def get_list(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        f2=soup.find('div',class_="f2")
        if f2:
            sq_jxs=f2.find('div',class_="sq_jxs_tab1")
            newdatalist=sq_jxs.find('table',id="newdatalist")
            tr_info=newdatalist.find_all('tr',class_="stygd")
            for tr in tr_info:
                href=tr.find('td',class_="p10").find('div',class_="pic").find('a').get('href')
                yield Request(self.dealer_url%href,callback=self.get_dealer_url)


    def get_dealer_url(self,response):
        result=XcarDealerPriceItem()
        soup = BeautifulSoup(response.body_as_unicode())
        tit=soup.find('title').get_text().strip()
        url=response.url
        result['tit']=tit
        result['url']=url
        result['category']='经销商-车型报价'
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













