# -*- coding: utf-8 -*-

from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from bs4 import BeautifulSoup
import re
import time
import json
from xcar_tit.items import XcarBrandvideoUrlItem
from xcar_tit import pipelines
from xcar_tit.Mongodb import monogoservice

class XcarBrandVideoSpider(RedisSpider):
    name = 'xcar_video'
    api_url='http://newcar.xcar.com.cn%s'
    pipeline = set([pipelines.XcarVideoPipeline, ])

    def start_requests(self):
        video_url=monogoservice.get_video_url()
        for url in video_url:
            yield Request(self.api_url%url, dont_filter=True, callback=self.get_letter)
            yield Request(self.api_url%url, callback=self.get_url)


    def get_letter(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        ul_info=soup.find('div',class_="video_tab").find('ul',class_="video-list mt20 clearfix")
        li_info=ul_info.find_all('li')
        if li_info:
            for li in li_info:
                href=li.find('a').get('href')
                yield Request(href,callback=self.get_url)

    def get_url(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        result = XcarBrandvideoUrlItem()
        url=response.url
        tit=soup.find('title').get_text().strip()
        place=soup.find('div',class_="place")
        if place:
            text=place.get_text().strip()
            add = text.split(':')
            result['address'] = add[1]
        xtv_position = soup.find('div', class_="xtv_position")
        if xtv_position:
            texts = xtv_position.get_text().strip()
            address = texts.split(':')
            result['address'] = address[1]
        result['category'] = '车系-视频'
        result['tit']=tit
        result['url']=url
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