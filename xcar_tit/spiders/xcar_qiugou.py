# -*- coding: utf-8 -*-

from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from bs4 import BeautifulSoup
import re
import time
import json
from xcar_tit.items import XcarDealerQiuGouItem
from xcar_tit import pipelines


class XcarQiuGouSpider(RedisSpider):
    name = 'xcar_qiugou'
    get_url='http://used.xcar.com.cn/qiugou/'
    api_url='http://used.xcar.com.cn%s'
    pipeline = set([pipelines.XcarQiugouPipeline, ])

    def start_requests(self):
        yield Request(self.get_url,dont_filter=True,callback=self.get_page_letter)
        yield Request(self.get_url,callback=self.get_urls)

    def get_page_letter(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        buycar_screen=soup.find('div',class_="buycar_screen")
        total=buycar_screen.find('h2').find('strong').get_text().strip()
        num=int(total)
        page_amount=num/10
        for page_num in range(page_amount+2):
            url='%s?RequestBuy_page=%d'%(response.url,page_num)
            yield Request(url,callback=self.get_list)

    def get_list(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        tr_info=soup.find('table',class_="table_border2").find_all('tr')
        for tr in tr_info:
            href=tr.find('td').find('a').get('href')
            yield Request(self.api_url%href,callback=self.get_urls)

    def get_urls(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        result = XcarDealerQiuGouItem()
        tit = soup.find('title').get_text().strip()
        url = response.url
        crumbs = soup.find('div', class_="crumbs")
        if crumbs:
            text = crumbs.get_text().strip()
            add = text.split('：')
            result['address'] = add[1]
        result['tit'] = tit
        result['url'] = url
        result['category'] = '求购信息'
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




