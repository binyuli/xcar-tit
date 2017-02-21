# -*- coding: utf-8 -*-

from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from bs4 import BeautifulSoup
import re
import time
import json
from xcar_tit.Mongodb import monogoservice

class XcarBrandlistSpider(RedisSpider):
    name = 'xcar_brandlist'
    get_url="http://newcar.xcar.com.cn/price/"
    api_url="http://newcar.xcar.com.cn%s"


    def start_requests(self):
        yield Request(self.get_url,headers={'Host': 'newcar.xcar.com.cn',
                                                           'Connection': 'keep-alive',
                                                           'Cache-Control': 'max-age=0',
                                                           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                                                           'X-Requested-With': 'XMLHttpRequest',
                                                           'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
                                                           'Accept-Encoding': 'gzip, deflate',
                                                           'Accept-Language': 'en-US,en;q=0.5'
                                                           },callback=self.get_brandlist)


    def get_brandlist(self,response):
        soup=BeautifulSoup(response.body_as_unicode())
        tbody=soup.find_all('tbody')
        for t in tbody:
            tr_info=t.find_all('tr')
            for tr in tr_info:
                href=tr.find('div',class_="column_tit").find('a').get('href')
                bid=href[9:-1]
                column_content=tr.find_all('div',class_="column_content")
                for column in column_content:
                    item_list=column.find_all('div',class_="item_list")
                    for items in item_list:
                        url=items.find('a').get('href')
                        cid=url[1:-1]
                        yield Request(self.api_url%url,meta={'bid':bid,'cid':cid},callback=self.get_brand)


    def get_brand(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        result=dict()
        bid=response.meta['bid']
        cid=response.meta['cid']

        tt_nav=soup.find('ul',class_="tt_nav")
        li_info=tt_nav.find_all('li')

        config_url = li_info[1].find('a').get('href')
        if config_url != 'javascript:void(0);':
            result['config_url'] = config_url

        pic_url = li_info[2].find('a').get('href')
        if pic_url != 'javascript:void(0);':
            result['pic_url'] = pic_url

        baojia_url = li_info[3].find('a').get('href')
        if baojia_url != 'javascript:void(0);':
            result['baojia_url'] = baojia_url

        vehicle_url = li_info[4].find('a').get('href')
        if vehicle_url != 'javascript:void(0);':
            result['vehicle_url'] = vehicle_url

        koubei_url=li_info[5].find('a').get('href')
        if koubei_url!='javascript:void(0);':
            result['koubei_url']=koubei_url

        article_url=li_info[6].find('a').get('href')
        if article_url!='javascript:void(0);':
            result['article_url']=article_url

        video_url = li_info[7].find('a').get('href')
        if video_url != 'javascript:void(0);':
            result['video_url'] = video_url

        baoyang_url = li_info[8].find('a').get('href')
        if baoyang_url != 'javascript:void(0);':
            result['baoyang_url'] = baoyang_url

        forum_url=li_info[10].find('a').get('href')
        if forum_url!='javascript:void(0);':
            result['forum_url']=forum_url

        result['bid']=bid
        result['cid']=cid

        put_result = json.dumps(dict(result), ensure_ascii=False, sort_keys=True, encoding='utf8').encode('utf8')
        save_result=json.loads(put_result)
        monogoservice.save_brandlist(save_result)


    def spider_idle(self):
        """This function is to stop the spider"""
        self.logger.info('the queue is empty, wait for one minute to close the spider')
        time.sleep(60)
        req = self.next_requests()

        if req:
            self.schedule_next_requests()
        else:
            self.crawler.engine.close_spider(self, reason='finished')


