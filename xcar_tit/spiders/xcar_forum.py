# -*- coding: utf-8 -*-

from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from bs4 import BeautifulSoup
import re
import time
import json
from xcar_tit.items import XcarForumItem

class XcarForumSpider(RedisSpider):
    name = 'xcar_forum'
    get_url='http://www.xcar.com.cn/bbs/'
    api_url='http://www.xcar.com.cn%s'

    def start_requests(self):
        yield Request(self.get_url,callback=self.get_letter)

    def get_letter(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        pinpaitab=soup.find_all('table', class_="t0922_pinpaitab")
        for tab in pinpaitab:
            pidiva=tab.find_all('div',class_="t0922_pidiva")
            for pid in pidiva:
                href=pid.find('span',id="w959").find('a').get('href')
                yield Request(href,callback=self.get_list)

        border_info=soup.find_all('div',class_="goCarBorder")
        for border in border_info:
            li_info=border.find('ul',class_="price_intro").find_all('li')
            for li in li_info:
                a_info=li.find('a')
                if a_info:
                    href=a_info.get('href')
                    yield Request(href,callback=self.get_list)


    def get_list(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        ul_info=soup.find('div',class_="navDiv").find('ul',class_="navtab clearfix")
        if ul_info:
            a_info=ul_info.find_all('a')
            for infos in a_info:
                onclick=infos.get('onclick')
                if onclick:
                    href=infos.get('href')
                    yield Request(self.api_url%href,callback=self.get_page_list)


    def get_page_list(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        page_info=soup.find('div',class_="fn_0209")
        if not page_info:
            page_amount=1
        else:
            info=page_info.find_all('a')
            if info:
                m=info[-2].get_text().strip()
                page_amount=int(m)
            else:
                page_amount=1
        url = response.url[:-5]
        for page_num in range(page_amount+1):
            urls=url+str(page_num)+'.html'
            yield Request(urls,callback=self.get_forum_list)


    def get_forum_list(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        f_box=soup.find('div',id="F_box_1")
        table_list=f_box.find_all('table',class_="row" )
        for table in table_list:
            tr_info=table.find_all('tr')
            href=tr_info[1].find('td',width="4%").find('a').get('href')
            yield Request(self.api_url%href,callback=self.get_urls)


    def get_urls(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        tit=soup.find('title').get_text().strip()
        url=response.url
        result=XcarForumItem()
        ph4 = soup.find('div',class_="p-h4")
        if ph4:
            text = ph4.get_text().strip()
            result['address'] = text
        result['tit'] = tit
        result['url'] = url
        result['category'] = '论坛'
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








