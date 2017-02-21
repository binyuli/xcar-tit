# -*- coding: utf-8 -*-

from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from bs4 import BeautifulSoup
import re
import time
import json
from xcar_tit.items import XcarBrandinfoUrlItem
from xcar_tit import pipelines


class XcarBrandinfoSpider(RedisSpider):
    name = 'xcar_brandinfo'
    get_url = "http://newcar.xcar.com.cn/price/"
    api_url = "http://newcar.xcar.com.cn%s"
    pipeline = set([pipelines.XcarBrandInfoPipeline, ])

    def start_requests(self):
        yield Request(self.get_url, headers={'Host': 'newcar.xcar.com.cn',
                                             'Connection': 'keep-alive',
                                             'Cache-Control': 'max-age=0',
                                             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                                             'X-Requested-With': 'XMLHttpRequest',
                                             'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
                                             'Accept-Encoding': 'gzip, deflate',
                                             'Accept-Language': 'en-US,en;q=0.5'
                                             }, callback=self.get_brandlist)


    def get_brandlist(self, response):
        soup = BeautifulSoup(response.body_as_unicode())
        tbody = soup.find_all('tbody')
        for t in tbody:
            tr_info = t.find_all('tr')
            for tr in tr_info:
                column_content = tr.find_all('div', class_="column_content")
                for column in column_content:
                    item_list = column.find_all('div', class_="item_list")
                    for items in item_list:
                        url = items.find('a').get('href')
                        yield Request(self.api_url % url,callback=self.get_urls)


    def get_urls(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        result = XcarBrandinfoUrlItem()
        url=response.url
        tit=soup.find('title').get_text().strip()
        place=soup.find('div',class_="place")
        if place:
            text=place.get_text().strip()
            add = text.split(':')
            result['address'] = add[1]
        result['category'] = '车系首页'
        result['tit']=tit
        result['url']=url
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


