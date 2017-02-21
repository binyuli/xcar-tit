# -*- coding: utf-8 -*-

from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from bs4 import BeautifulSoup
import re
import time
import json
from xcar_tit.items import XcarInstituteItem
from xcar_tit import pipelines


class XcarInstituteSpider(RedisSpider):
    name = 'xcar_institute'
    get_url='http://info.xcar.com.cn/push_556/'
    news_url='http://info.xcar.com.cn/great/ajax.php?time=1486628336950&cate_id=556&page=1&part=%d'
    pipeline = set([pipelines.XcarInstitutePipeline, ])

    def start_requests(self):
        yield Request(self.get_url,dont_filter=True,callback=self.get_letter)
        yield Request(self.get_url,callback=self.get_urls)

    def get_letter(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        num=soup.find('div',class_="nr_con").find('div',class_="clearfix").find('div',class_="fr").find('span').get_text().strip()
        pageinfo=int(num)
        page_amount=pageinfo/5
        for page_num in range(page_amount+1):
            url=self.news_url%page_num
            yield Request(url,callback=self.get_list)

    def get_list(self,response):
        soup = BeautifulSoup(response.body)
        li_info=soup.find_all('li')
        for li in li_info:
            href=li.find('a').get('href')
            yield Request(href,callback=self.get_urls)

    def get_urls(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        tit=soup.find('title').get_text().strip()
        url=response.url
        result=XcarInstituteItem()
        p1 = soup.find('div', class_="p1")
        if p1:
            text = p1.get_text().strip()
            address = text.split('：')
            result['address'] = address[1]
        result['tit'] = tit
        result['url'] = url
        result['category'] = '爱卡研究院'
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