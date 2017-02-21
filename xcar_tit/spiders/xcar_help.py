# -*- coding: utf-8 -*-

from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from bs4 import BeautifulSoup
import re
import time
import json
from xcar_tit.items import XcarHelpItem
from xcar_tit import pipelines

class XcarHelpSpider(RedisSpider):
    name = 'xcar_help'
    get_url='http://info.xcar.com.cn/push_566/'
    api_url='http://info.xcar.com.cn/info_index.php?c=special&m=help&page=%d'
    pipeline = set([pipelines.XcarHelpPipeline, ])

    def start_requests(self):
        yield Request(self.get_url,dont_filter=True,callback=self.get_letter)
        yield Request(self.get_url,callback=self.get_urls)

    def get_letter(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        pageinfo=soup.find('div',id='t_0915_ipage')
        if not pageinfo:
            page_amount=1
        else:
            page_info=pageinfo.find_all('a')
            if page_info:
                m=page_info[-2].get_text().strip()
                page_amount=int(m)
            else:
                page_amount=1
        for page_num in range(1,page_amount+1):
            url=self.api_url%page_num
            yield Request(url,callback=self.get_list)

    def get_list(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        past_reseach=soup.find('div',class_="past_reseach")
        if past_reseach:
            li_info=past_reseach.find('ul',class_="pr_list").find_all('li')
            for li in li_info:
                href=li.find('a').get('href')
                yield Request(href,callback=self.get_urls)

    def get_urls(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        tit=soup.find('title').get_text().strip()
        url=response.url
        result=XcarHelpItem()
        p1 = soup.find('div', class_="p1")
        if p1:
            text = p1.get_text().strip()
            address = text.split('：')
            result['address'] = address[1]
        result['tit'] = tit
        result['url'] = url
        result['category'] = '爱卡来帮你'
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



