# -*- coding: utf-8 -*-

from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from bs4 import BeautifulSoup
import re
import time
import json
from xcar_tit.Mongodb import monogoservice

class XcarDealerSpider(RedisSpider):
    name = 'xcar_dealer'
    api_url='http://dealer.xcar.com.cn/'
    dealer_url='http://dealer.xcar.com.cn%s'


    def start_requests(self):
        yield Request(self.api_url,callback=self.get_letter)


    def get_letter(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        ulcon_info=soup.find_all('div',class_="ulcon")
        for ulcon in ulcon_info[1:]:
            a_info=ulcon.find_all('a')
            for info in a_info:
                href=info.get('href')
                yield Request(self.dealer_url%href,callback=self.get_page_letter)


    def get_page_letter(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        unify_page=soup.find_all('div',class_="unify_page")
        if unify_page:
            if len(unify_page)>1:
                page_info=unify_page[0]
                a_info=page_info.find_all('a')
                page_amount = a_info[-2].get_text().strip()
                for page_num in range(1,int(page_amount)+1):
                    url='%s?type=1&page=%d'%(response.url,page_num)
                    yield Request(url,callback=self.get_dealer_list)

                a_infos = page_info.find_all('a')
                page_amounts = a_infos[-2].get_text().strip()
                for page_num in range(1,int(page_amounts) + 1):
                    url = '%s?type=2&page=%d' % (response.url, page_num)
                    yield Request(url, callback=self.get_dealer_lists)
            else:
                pageinfo=unify_page[0]
                a_info = pageinfo.find_all('a')
                page_amount = a_info[-2].get_text().strip()
                for page_num in range(1,int(page_amount) + 1):
                    url = '%s?type=1&page=%d' % (response.url, page_num)
                    yield Request(url, callback=self.get_dealer_list)


    def get_dealer_list(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        dealer_list=soup.find('div',id="dlists_4s_isfee").find('ul')
        if dealer_list:
            li_info=dealer_list.find_all('li')
            for li in li_info:
                href=li.find('a').get('href')
                yield Request(self.dealer_url%href,callback=self.get_dealer)


    def get_dealer_lists(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        dealer_list=soup.find('div',id="dlists_zh").find('ul')
        if dealer_list:
            li_info=dealer_list.find_all('li')
            for li in li_info:
                href=li.find('a').get('href')
                yield Request(self.dealer_url%href,callback=self.get_dealer)


    def get_dealer(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        ul_info=soup.find('div',class_="jxs10_menu").find('ul')
        if ul_info:
            result=dict()
            li_info=ul_info.find_all('li')
            for li in li_info:
                href=li.find('a')
                url=href.get('href')
                if url:
                    if 'activity' in url:
                        result['activity_url'] = url
                    elif 'ershouche' in url:
                        result['usedcar_url'] = url
                    elif 'price' in url:
                        result['price_url'] = url
                    elif 'news' in url:
                        result['news_url'] = url
                    elif 'about' in url:
                        result['about_url'] = url
                    elif 'comment' in url:
                        result['comment_url'] = url
                    elif 'photo' in url:
                        result['photo_url'] = url
                    elif 'proprice' in url:
                        result['proprice_url'] = url
                    else:
                        result['index_url'] = url
                onclick=href.get('onclick')
                if onclick:
                    if 'dianping' in onclick:
                        result['dianping_url'] = onclick[17:-1]
                    elif 'repair' in onclick:
                        result['repair_url'] = onclick[17:-1]

            put_result = json.dumps(dict(result), ensure_ascii=False, sort_keys=True, encoding='utf8').encode('utf8')
            save_result = json.loads(put_result)
            monogoservice.save_dealerlist(save_result)


    def spider_idle(self):
        """This function is to stop the spider"""
        self.logger.info('the queue is empty, wait for one minute to close the spider')
        time.sleep(30)
        req = self.next_requests()

        if req:
            self.schedule_next_requests()
        else:
            self.crawler.engine.close_spider(self, reason='finished')






























