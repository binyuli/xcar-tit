# -*- coding: utf-8 -*-

from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from bs4 import BeautifulSoup
import re
import time
import json
from xcar_tit.items import XcarDealerIndexItem
from xcar_tit import pipelines

class XcarDealerIndexSpider(RedisSpider):
    name = 'xcar_dealerindex'
    api_url = 'http://dealer.xcar.com.cn/'
    dealer_url = 'http://dealer.xcar.com.cn%s'
    pipeline = set([pipelines.XcarDealerIndexPipeline, ])


    def start_requests(self):
        yield Request(self.api_url,callback=self.get_letter)


    def get_letter(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        ulcon_info=soup.find_all('div',class_="ulcon")
        for ulcon in ulcon_info[1:]:
            a_info=ulcon.find_all('a')
            for info in a_info:
                href=info.get('href')
                yield Request(self.dealer_url%href,callback=self.get_page_letter)


    def get_page_letter(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        unify_page=soup.find_all('div',class_="unify_page")
        if unify_page:
            if len(unify_page)>1:
                page_info=unify_page[0]
                a_info=page_info.find_all('a')
                page_amount = a_info[-2].get_text().strip()
                for page_num in range(int(page_amount)+1):
                    url='%s?type=1&page=%d'%(response.url,page_num)
                    yield Request(url,callback=self.get_dealer_list)

                a_infos = page_info.find_all('a')
                page_amounts = a_infos[-2].get_text().strip()
                for page_num in range(int(page_amounts) + 1):
                    url = '%s?type=2&page=%d' % (response.url, page_num)
                    yield Request(url, callback=self.get_dealer_lists)
            else:
                pageinfo=unify_page[0]
                a_info = pageinfo.find_all('a')
                page_amount = a_info[-2].get_text().strip()
                for page_num in range(int(page_amount) + 1):
                    url = '%s?type=1&page=%d' % (response.url, page_num)
                    yield Request(url, callback=self.get_dealer_list)


    def get_dealer_list(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        dealer_list=soup.find('div',id="dlists_4s_isfee").find('ul')
        if dealer_list:
            li_info=dealer_list.find_all('li')
            for li in li_info:
                href=li.find('a').get('href')
                yield Request(self.dealer_url%href,callback=self.get_dealer)


    def get_dealer_lists(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        dealer_list=soup.find('div',id="dlists_zh").find('ul')
        if dealer_list:
            li_info=dealer_list.find_all('li')
            for li in li_info:
                href=li.find('a').get('href')
                yield Request(self.dealer_url%href,callback=self.get_dealer)


    def get_dealer(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        result=XcarDealerIndexItem()
        tit=soup.find('title')
        url=response.url
        result['tit']=tit
        result['url']=url
        result['category']='经销商-首页'
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
