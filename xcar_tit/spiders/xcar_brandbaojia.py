# -*- coding: utf-8 -*-

from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from bs4 import BeautifulSoup
import re
import time
import json
from xcar_tit.Mongodb import monogoservice
from xcar_tit.items import XcarBrandbaojiaUrlItem
from xcar_tit import pipelines

class XcarBrandBaojiaSpider(RedisSpider):
    name = 'xcar_baojia'
    api_url='http://newcar.xcar.com.cn%s'
    baojia_url='http://newcar.xcar.com.cn/auto/index.php?r=newcar/SeriseParentPrice/AjaxStopSaleModel&pserid=%s&year=%s'
    pipeline = set([pipelines.XcarBrandBaojiaPipeline, ])

    def start_requests(self):
        baojia_urls=monogoservice.get_baojia_url()
        for brand in baojia_urls:
            url=brand['baojia_url']
            cid = brand['cid']
            yield Request(self.api_url%url, dont_filter=True,meta={'cid': cid}, callback=self.get_letter)
            yield Request(self.api_url%url, callback=self.get_url)


    def get_letter(self,response):
        cid=response.meta['cid']
        soup = BeautifulSoup(response.body_as_unicode())
        demio_main=soup.find('div',class_="demio_cl").find('div',class_="demio_main")
        modellist_open=demio_main.find('table')
        if modellist_open:
            tr_info=modellist_open.find('tbody').find_all('tr',class_="table_bord")
            for tr in tr_info:
                href=tr.find('td').find('p').find('a').get('href')
                yield Request(self.api_url%href,callback=self.get_url)

        stop_pop=demio_main.find('div',class_="demio_tt bd_b").find('div',class_="stop_pop")
        if stop_pop:
            li_info=stop_pop.find_all('li')
            for li in li_info:
                year=li.find('a').get('data')
                url=self.baojia_url%(cid,year)
                yield Request(url,callback=self.get_list)


    def get_list(self,response):
        soup = BeautifulSoup(response.body)
        modellist_open = soup.find('table', class_="table_main")
        tr_info = modellist_open.find('tbody').find_all('tr', class_="table_bord")
        for tr in tr_info:
            href = tr.find('td').find('p').find('a').get('href')
            yield Request(self.api_url%href, callback=self.get_url)


    def get_url(self,response):
        result=XcarBrandbaojiaUrlItem()
        soup = BeautifulSoup(response.body_as_unicode())
        tit=soup.find('title').get_text()
        place=soup.find('div',class_="place")
        if place:
            text = place.get_text().strip()
            add = text.split(':')
            result['address'] = add[1]
        url=response.url
        result['category'] = '车系-报价'
        result['tit'] = tit
        result['url'] = url
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