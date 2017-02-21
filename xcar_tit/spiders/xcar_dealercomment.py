# -*- coding: utf-8 -*-

from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from bs4 import BeautifulSoup
import re
import time
import json
from xcar_tit.items import XcarDealerCommentItem
from xcar_tit.Mongodb import monogoservice
from xcar_tit import pipelines


class XcarDealerCommentSpider(RedisSpider):
    name = 'xcar_dealercomment'
    dealer_url = 'http://dealer.xcar.com.cn%s'
    pipeline = set([pipelines.XcarDealerCommentPipeline, ])

    def start_requests(self):
        comment_url=monogoservice.get_dealercomment_url()
        for url in comment_url:
            yield Request(self.dealer_url%url,dont_filter=True,callback=self.get_letter)
            yield Request(self.dealer_url%url,callback=self.get_url)


    def get_letter(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        page_info=soup.find('p',class_="t_0915_ipage")
        if not page_info:
            page_amount=1
        else:
            pageinfo=page_info.find_all('a')
            if not pageinfo:
                page_amount=1
            else:
                m=pageinfo[-2].get_text().strip()
                page_amount=int(m)
        for page_num in range(1,page_amount+1):
            url=response.url[:-4]+'_'+str(page_num)+'.htm'
            yield Request(url,callback=self.get_url)


    def get_url(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        result=XcarDealerCommentItem()
        tit=soup.find('title').get_text().strip()
        url=response.url
        result['tit']=tit
        result['url']=url
        result['category']='经销商-购车问答'
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

