# -*- coding: utf-8 -*-

from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from bs4 import BeautifulSoup
import time
from xcar_tit.items import XcarBrandkoubeiUrlItem

class XcarKoubeiSpider(RedisSpider):
    name = 'xcar_koubei'
    get_url='http://newcar.xcar.com.cn%s'


    def start_requests(self):
        fi=open('xcar_tit/xcar_brandlist','r')
        for line in fi:
            brand_info=eval(line)
            if brand_info.has_key('koubei_url'):
                url=brand_info['koubei_url']
                yield Request(self.get_url%url,callback=self.get_letter)


    def get_letter(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        href=soup.find('div',id="content_title_div").find('a').get('href')
        yield Request(self.get_url%href,callback=self.get_page)


    def get_page(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        pagers=soup.find('div',class_="pagers")
        url=response.url
        new_url=url.replace(".htm", "/0_%d.htm")
        if not pagers:
            page_amount = 1
        else:
            div = pagers.find_all('a')
            num = div[-2].get_text().encode('utf-8')
            n = int(num)
            if not n:
                page_amount = 1
            else:
                page_amount = n
        for page_num in range(1, page_amount + 1):
            koubeiurl=new_url%page_num
            yield Request(koubeiurl,callback=self.get_koubeilist)


    def get_koubeilist(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        review_comments=soup.find('div',class_="review_comments_dl")
        dl_info=review_comments.find_all('dl')
        for dl in dl_info:
            dt_info=dl.find('dt').find_all('a')
            href=dt_info[-1].get('href')
            yield Request(href,callback=self.get_urls)


    def get_urls(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        result = XcarBrandkoubeiUrlItem()
        url=response.url
        tit=soup.find('title').get_text().strip()
        place=soup.find('span',class_="scrap_span")
        if place:
            text=place.get_text().strip()
            result['address'] = text
        p_h4 = soup.find('div', class_="p-h4")
        if p_h4:
            texts = p_h4.get_text().strip()
            result['address'] = texts
        result['category'] = '车系-口碑'
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


