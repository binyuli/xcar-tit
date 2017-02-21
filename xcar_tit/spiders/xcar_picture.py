# -*- coding: utf-8 -*-

from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from bs4 import BeautifulSoup
import re
import time
import json
from xcar_tit.items import XcarBrandpictureUrlItem
from xcar_tit import pipelines

class XcarBrandPictureSpider(RedisSpider):
    name = 'xcar_pic'
    pic_url='http://newcar.xcar.com.cn/photo/'
    api_url='http://newcar.xcar.com.cn%s'
    pipeline = set([pipelines.XcarPicturePipeline, ])

    def start_requests(self):
        yield Request(self.pic_url,callback=self.get_letter)


    def get_letter(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        li_info=soup.find('div',id="treebox_list").find('div',class_="fra_box_lt").find_all('li')
        for li in li_info:
            a_info=li.find('a')
            if a_info:
                href=a_info.get('href')
                yield Request(self.api_url%href,dont_filter=True,callback=self.get_brand_list)
                yield Request(self.api_url%href,callback=self.get_url)

    def get_brand_list(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        li_info = soup.find('div', id="treebox_list").find('div', class_="fra_box_lt").find_all('li')
        for li in li_info:
            ul_info = li.find('ul')
            if ul_info:
                li_infos = ul_info.find_all('li',class_="menu_li")
                for lis in li_infos:
                    href=lis.find('a').get('href')
                    yield Request(self.api_url % href,dont_filter=True, callback=self.get_type_list)
                    yield Request(self.api_url % href, callback=self.get_url)


    def get_type_list(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        ul_info = soup.find('div', class_="pic_tabs").find('ul', class_="pic_tabs_menu")
        li_info = ul_info.find_all('li')
        for li in li_info:
            href=li.find('a').get('href')
            yield Request(self.api_url % href, dont_filter=True,callback=self.get_car_list)
            yield Request(self.api_url % href, callback=self.get_url)


    def get_car_list(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        pic_c_item = soup.find('div', class_="pic_choose").find('dl', class_="pic_c_item clearfix")
        pic_info = pic_c_item.find('dd', class_="clearfix").find_all('a')
        for pic in pic_info:
            url = pic.get('href')
            yield Request(self.api_url % url, dont_filter=True, callback=self.get_vehicle_list)
            yield Request(self.api_url % url, callback=self.get_url)


    def get_vehicle_list(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        pic_c_item = soup.find('div', class_="pic_choose").find_all('dl', class_="pic_c_item clearfix")
        for dl in pic_c_item:
            pic_c_class=dl.find('dd', class_="clearfix").find('div',class_="pic_c_class")
            if pic_c_class:
                dd_info = pic_c_class.find_all('a')
                for dd in dd_info:
                    href=dd.get('href')
                    yield Request(self.api_url%href,dont_filter=True,callback=self.get_page_list)
                    yield Request(self.api_url%href,callback=self.get_url)


    def get_page_list(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        sort_page=soup.find('div',class_="sort-page")
        if not sort_page:
            page_amount = 1
        else:
            nums=sort_page.find_all('a')
            num=nums[-2].get_text().strip()
            m=int(num)
            if not m:
                page_amount = 1
            else:
                page_amount = m

        for page_num in range(1, page_amount + 1):
            url = response.url
            page_url='%s?page=%d'%(url,page_num)
            yield Request(page_url,callback=self.get_pic_list)


    def get_pic_list(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        dl_info=soup.find('div',class_="pic-con").find_all('dl')
        for dl in dl_info:
            href=dl.find('dt').find('a').get('href')
            yield Request(self.api_url%href,callback=self.get_url)


    def get_url(self,response):
        result=XcarBrandpictureUrlItem()
        soup = BeautifulSoup(response.body_as_unicode())
        tit=soup.find('title').get_text()
        crumb_nt=soup.find('div',class_="atlas_nav")
        if crumb_nt:
            text = crumb_nt.get_text().strip()
            add = text.split('：')
            result['address'] = add[1].strip()
        titleLeft=soup.find('span' ,class_="titleLeft")
        if titleLeft:
            text = titleLeft.get_text().strip()
            address = text.split('：')
            result['address'] = address[1].strip()
        url=response.url
        result['category'] = '车系-图片'
        result['tit'] = tit
        result['url'] = url
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