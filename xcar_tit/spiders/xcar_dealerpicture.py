# -*- coding: utf-8 -*-

from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from bs4 import BeautifulSoup
import re
import time
import json
from xcar_tit.items import XcarDealerPictureItem
from xcar_tit.Mongodb import monogoservice
from xcar_tit import pipelines

class XcarDealerPictureSpider(RedisSpider):
    name = 'xcar_dealerpic'
    dealer_url='http://dealer.xcar.com.cn%s'
    pipeline = set([pipelines.XcarDealerPicturePipeline, ])

    def start_requests(self):
        pic_url=monogoservice.get_dealerpic_url()
        for url in pic_url:
            yield Request(self.dealer_url%url,dont_filter=True,callback=self.get_letter)
            yield Request(self.dealer_url%url,callback=self.get_url)

    def get_letter(self,response):
        soup=BeautifulSoup(response.body_as_unicode())
        jxs_zypp=soup.find('div',class_="jxs_zypp")
        if jxs_zypp:
            brand_more=jxs_zypp.find('div',class_="n").find('div',class_="brand_more")
            ul_info=brand_more.find_all('ul',class_="jxs_l3")
            for ul in ul_info:
                li_info=ul.find_all('li')
                for li in li_info[2:]:
                    href=li.find('a').get('href')
                    yield Request(self.dealer_url%href,dont_filter=True,callback=self.get_pic_list)
                    yield Request(self.dealer_url%href,callback=self.get_url)

    def get_pic_list(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        bt_info=soup.find('div',class_="jxs_pic2").find_all('h4',class_="bt")
        for bt in bt_info:
            href=bt.find('em').find('a').get('href')
            yield Request(self.dealer_url%href,dont_filter=True,callback=self.get_page_list)
            yield Request(self.dealer_url%href,callback=self.get_url)


    def get_page_list(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        page_info=soup.find('p',class_="t_0915_ipage")
        if not page_info:
            page_amount=1
        else:
            a_info=page_info.find_all('a')
            m=a_info[-2].get_text().strip()
            if not m:
                page_amount=1
            else:
                page_amount=int(m)
        for page_num in range(page_amount+1):
            url=response.url[:-5]+str(page_num)+'.htm'
            yield Request(url,callback=self.get_pic)


    def get_pic(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        jxs_pic=soup.find('div',class_="jxs_pic2")
        if jxs_pic:
            ul_info=jxs_pic.find_all('ul',class_="l3")
            for ul in ul_info:
                li_info=ul.find_all('li')
                for li in li_info:
                    href=li.find('a').get('href')
                    yield Request(self.dealer_url%href,callback=self.get_url)


    def get_url(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        tit=soup.find('title').get_text().strip()
        url=response.url
        result=XcarDealerPictureItem()
        np_menu=soup.find('p',class_="np_menu")
        if np_menu:
            text=np_menu.get_text().strip()
            add = text.split('：')
            result['address'] = add[1]
        result['tit']=tit
        result['url']=url
        result['category'] = '经销商-车型图片'
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







