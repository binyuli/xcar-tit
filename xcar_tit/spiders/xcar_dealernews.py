# -*- coding: utf-8 -*-

from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from bs4 import BeautifulSoup
import re
import time
import json
from xcar_tit.items import XcarDealerNewsItem
from xcar_tit.Mongodb import monogoservice
from xcar_tit import pipelines

class XcarDealerNewsSpider(RedisSpider):
    name = 'xcar_dealernews'
    dealer_url='http://dealer.xcar.com.cn%s'
    pipeline = set([pipelines.XcarDealerNewsPipeline, ])

    def start_requests(self):
        news_url=monogoservice.get_dealernews_url()
        for url in news_url:
            yield Request(self.dealer_url%url,dont_filter=True,callback=self.get_letter)
            yield Request(self.dealer_url%url,callback=self.get_news)


    def get_letter(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        jxs_esc=soup.find('div',class_="jxs_esc_l")
        if jxs_esc:
            i_info=jxs_esc.find('h3',class_="jxs_bt42").find_all('i')
            for infos in i_info:
                href=infos.find('a').get('href')
                yield Request(self.dealer_url%href,callback=self.get_page_list)


    def get_page_list(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        page_info=soup.find('p',class_="t_0915_ipage")
        if not page_info:
            page_amount=1
        else:
            infos=page_info.find_all('a')
            m=infos[-2].get_text().strip()
            if not m:
                page_amount=1
            else:
                page_amount=int(m)
        for page_num in range(1,page_amount+1):
            url=response.url[:-5]+str(page_num)+'.htm'
            yield Request(url,callback=self.get_news_list)


    def get_news_list(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        jxs_esc_n=soup.find('div',class_="jxs_esc_n")
        if jxs_esc_n:
            li_info=jxs_esc_n.find('ul',class_="la").find_all('li')
            for li in li_info:
                href=li.find('a').get('href')
                yield Request(self.dealer_url%href,callback=self.get_news)


    def get_news(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        tit=soup.find('title').get_text().strip()
        url= response.url
        result=XcarDealerNewsItem()
        result['tit']=tit
        result['url']=url
        result['category']='经销商-促销信息'
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














