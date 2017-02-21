# -*- coding: utf-8 -*-

from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from bs4 import BeautifulSoup
import re
import time
import json
from xcar_tit import pipelines
from xcar_tit.items import XcarActivityItem


class XcarActivitySpider(RedisSpider):
    name = 'xcar_activity'
    get_url='http://club.xcar.com.cn/active/'
    api_url='http://club.xcar.com.cn%s'
    pipeline = set([pipelines.XcarActivityPipeline, ])

    def start_requests(self):
        yield Request(self.get_url,dont_filter=True,callback=self.get_letter)
        yield Request(self.get_url,callback=self.get_urls)


    def get_letter(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        sort_item=soup.find('div',id="sml_title").find('div',class_="sort_item item_h35")
        if sort_item:
            a_info=sort_item.find_all('a')
            for info in a_info[1:]:
                href=info.get('href')
                yield Request(self.api_url%href,dont_filter=True,callback=self.get_page_list)
                yield Request(self.api_url%href,callback=self.get_page_list)


    def get_page_list(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        page_info=soup.find('div',class_="unify_page")
        if not page_info:
            return
        infos=page_info.find_all('a')
        if not infos:
            page_amount=1
        else:
            m=infos[-2].get_text().strip()
            page_amount=int(m)
        url=response.url[:-1]
        for page_num in range(page_amount+1):
            urls=url+'_'+str(page_num)+'/'
            yield Request(urls,callback=self.get_list)


    def get_list(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        column_left=soup.find('div',class_="column_left f_l")
        if column_left:
            column_cont=column_left.find('div',class_="column_cont").find('ul',class_="leftList")
            li_info=column_cont.find_all('li')
            for li in li_info:
                href=li.find('div',class_="listleftcon").find('a').get('href')
                yield Request(href,callback=self.get_urls)


    def get_urls(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        tit=soup.find('title').get_text().strip()
        url=response.url
        result=XcarActivityItem()
        ph4 = soup.find('div',class_="p-h4")
        if ph4:
            text = ph4.get_text().strip()
            result['address'] = text
        result['tit'] = tit
        result['url'] = url
        result['category'] = '车友活动'
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




