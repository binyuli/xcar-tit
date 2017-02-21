# -*- coding: utf-8 -*-

from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from bs4 import BeautifulSoup
import re
import time
import json
from xcar_tit import pipelines
from xcar_tit.items import XcarWikiItem


class XcarWikiSpider(RedisSpider):
    name = 'xcar_wiki'
    get_url='http://yp.xcar.com.cn/wiki/'
    pipeline = set([pipelines.XcarWikiPipeline, ])


    def start_requests(self):
        yield Request(self.get_url,dont_filter=True,callback=self.get_letter)
        yield Request(self.get_url,callback=self.get_urls)


    def get_letter(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        wiki_z=soup.find('div',class_="wiki_z").find('div',class_="wiki_sidebar f_l")
        wiki_tree=wiki_z.find_all('ul',class_="wiki_tree")
        for tree in wiki_tree:
            li_info=tree.find_all('li')
            for li in li_info:
                ul_info=li.find('ul',class_="side_roll")
                if ul_info:
                    href=ul_info.find('li').find('a').get('href')
                    yield Request(href,callback=self.get_urls)


    def get_urls(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        tit=soup.find('title').get_text().strip()
        url=response.url
        result = XcarWikiItem()
        wiki_bread = soup.find('div', class_="wiki_bread")
        if wiki_bread:
            text = wiki_bread.get_text().strip()
            add = text.split('：')
            result['address'] = add[1]
        result['tit'] = tit
        result['url'] = url
        result['category'] = '汽车知识库'
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