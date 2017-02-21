# -*- coding: utf-8 -*-

from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from bs4 import BeautifulSoup
import re
import time
import json
from xcar_tit.items import XcarPhotoItem
from xcar_tit import pipelines


class XcarPhotoSpider(RedisSpider):
    name = 'xcar_photo'
    get_url='http://photo.xcar.com.cn/'
    api_url='http://photo.xcar.com.cn%s'
    photo_url='http://photo.xcar.com.cn/group/view_t.php?pid=%d'
    pipeline = set([pipelines.XcarPhotoPipeline, ])

    def start_requests(self):
        yield Request(self.get_url,dont_filter=True,callback=self.get_letter)
        yield Request(self.get_url,callback=self.get_urls)

    def get_letter(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        pictor_navlist=soup.find('div',class_="pictor_navlist clearfix")
        if pictor_navlist:
            li_info=pictor_navlist.find('ul',class_="mid_title_small clearfix").find_all('li')
            for li in li_info:
                href=li.find('a').get('href')
                yield Request(href,callback=self.get_page_list)

    def get_page_list(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        fr=soup.find('div',class_="hpic_wrap bc").find('div',class_="hpic_posi").find('div',class_="fr").find('div',class_="mt5")
        em_info=fr.find_all('em')
        text=em_info[1].get_text().strip()
        page_amount=text[1:-1]
        url=response.url[:-1]
        for page_num in range(1,int(page_amount)+1):
            urls=url+'_'+str(page_num)+'/'
            yield Request(urls,callback=self.get_list)

    def get_list(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        hpic_con=soup.find('div',class_="hpic_con")
        if hpic_con:
            li_info=hpic_con.find('ul',class_="h_newmap").find_all('li')
            for li in li_info:
                href=li.find('a').get('href')
                if 'http' in href:
                    yield Request(href, callback=self.get_photo)
                else:
                    yield Request(self.api_url%href,callback=self.get_photo)

    def get_photo(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        url=response.url
        if 'bbs' in url:
            img_cons=soup.find('div',class_="img_cons")
            if img_cons:
                li_info=img_cons.find('ul',class_="clearfix").find_all('li')
                for li in li_info:
                    id=li.find('table').find('img').get('id')
                    bbs_url=url[:-5]+id[3:]+'.htm'
                    yield Request(bbs_url, callback=self.get_urls)

        else:
            photo_list=soup.find('div',class_="photo_list")
            if photo_list:
                smaill_list=photo_list.find('div', id="SmallWarp").find('ul', id="Smailllist")
                li_info=smaill_list.find_all('li')
                if len(li_info)>1:
                    url=li_info[1].find('a').get('href')
                    num=re.findall(r'pid=(.+?)',url)
                    text=li_info[1].find('div').find('i').get_text().strip()
                    texts=text.split('/')
                    page=int(texts[1])+int(num[0])
                    for page_num in range(int(num[0]),page+1):
                        yield Request(self.photo_url%page_num,headers = {'Host':'photo.xcar.com.cn',
                            'Connection': 'keep-alive',
                           'Cache-Control': 'max-age=0',
                           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                           'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
                           'Accept-Encoding': 'gzip, deflate',
                           'Accept-Language': 'en-US,en;q=0.5'
                           },callback=self.get_urls)


    def get_urls(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        tit=soup.find('title').get_text().strip()
        url=response.url
        result=XcarPhotoItem()
        nav = soup.find('div', class_="nav")
        if nav:
            text = nav.get_text().strip()
            address = text.split('：')
            result['address'] = address[1]
        result['tit'] = tit
        result['url'] = url
        result['category'] = '视觉频道'
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











