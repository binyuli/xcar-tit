# -*- coding: utf-8 -*-

from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from bs4 import BeautifulSoup
import re
import time
import json
from xcar_tit.items import XcarTechItem
from xcar_tit import pipelines


class XcarTechSpider(RedisSpider):
    name = 'xcar_tech'
    get_url='http://tech.xcar.com.cn/'
    api_url='http://club.xcar.com.cn%s'
    pipeline = set([pipelines.XcarTechPipeline, ])

    def start_requests(self):
        yield Request(self.get_url,callback=self.get_letter)

    def get_letter(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        tnav_style=soup.find('div',class_="tnav_style1 noliststyle")
        if tnav_style:
            li_info=tnav_style.find_all('li')
            for li in li_info[1:]:
                href=li.find('a').get('href')
                yield Request(href,callback=self.get_type)

    def get_type(self,response):
        url=response.url
        if '644' in url:
            page_amount=39
        elif '643' in url:
            page_amount=10
        elif '884' in url:
            page_amount=18
        else:
            page_amount=6

        for page_num in range(1,page_amount+1):
            page_url=url[:-1]+'_'+str(page_num)+'/'
            yield Request(page_url,callback=self.get_list)

    def get_list(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        remark_left=soup.find('div',class_="remark_left")
        if not remark_left:
            return
        ul_info=remark_left.find('ul',class_='leftList')
        if ul_info:
            li_info=ul_info.find_all('li',class_="clearfix moreImgSize")
            for li in li_info:
                href=li.find('div',class_="leftConSize").find('a').get('href')
                yield Request(href,callback=self.get_urls)


    def get_urls(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        tit=soup.find('title').get_text().strip()
        url=response.url
        result=XcarTechItem()
        p1 = soup.find('div', class_="p1")
        if p1:
            text = p1.get_text().strip()
            address = text.split('：')
            result['address'] = address[1]
        result['tit'] = tit
        result['url'] = url
        result['category'] = '科技资讯'
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





























