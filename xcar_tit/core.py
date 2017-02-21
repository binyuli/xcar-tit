# -*- coding: utf-8 -*-
import scrapy
import scrapy_redis

from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.conf import settings
from scrapy.utils.log import configure_logging

from spiders.xcar_activity import XcarActivitySpider
from spiders.xcar_book import XcarBookSpider
from spiders.xcar_brandbaojia import XcarBrandBaojiaSpider
from spiders.xcar_brandconfig import XcarBrandConfigSpider
from spiders.xcar_brandinfo import XcarBrandinfoSpider
from spiders.xcar_brandlist import XcarBrandlistSpider
from spiders.xcar_brandvehicle import XcarBrandvehicleSpider
from spiders.xcar_carprice import XcarDealerCarPriceSpider
from spiders.xcar_dealer import XcarDealerSpider
from spiders.xcar_dealerabout import XcarDealerAboutSpider
from spiders.xcar_dealeractivity import XcarDealerActivitySpider
from spiders.xcar_dealercomment import XcarDealerCommentSpider
from spiders.xcar_dealerdianping import XcarDealerDianPingSpider
from spiders.xcar_dealerindex import XcarDealerIndexSpider
from spiders.xcar_dealernews import XcarDealerNewsSpider
from spiders.xcar_dealerpicture import XcarDealerPictureSpider
from spiders.xcar_dealerprice import XcarDealerPriceSpider
from spiders.xcar_drive import XcarDriveSpider
from spiders.xcar_forum import XcarForumSpider
from spiders.xcar_green import XcarGreenSpider
from spiders.xcar_guide import XcarGuideSpider
from spiders.xcar_help import XcarHelpSpider
from spiders.xcar_index import XcarIndexSpider
from spiders.xcar_institute import XcarInstituteSpider
from spiders.xcar_koubei import XcarKoubeiSpider
from spiders.xcar_newcar import XcarNewCarSpider
from spiders.xcar_photo import XcarPhotoSpider
from spiders.xcar_picture import XcarBrandPictureSpider
from spiders.xcar_qiugou import XcarQiuGouSpider
from spiders.xcar_selected import XcarSelectedSpider
from spiders.xcar_suv import XcarSUVSpider
from spiders.xcar_tech import XcarTechSpider
from spiders.xcar_usedcar import XcarUsedcarSpider
from spiders.xcar_video import XcarBrandVideoSpider
from spiders.xcar_wiki import XcarWikiSpider
from spiders.xcar_xview import XcarXviewSpider
from spiders.xcar_yangche import XcarBrandyangcheSpider

import os
import pymongo
import json

# the spider we need to scheduler
ActivitySpider = XcarActivitySpider()
BookSpider = XcarBookSpider()
BrandBaojiaSpider = XcarBrandBaojiaSpider()
BrandConfigSpider = XcarBrandConfigSpider()
BrandinfoSpider = XcarBrandinfoSpider()
BrandlistSpider = XcarBrandlistSpider()
BrandvehicleSpider = XcarBrandvehicleSpider()
DealerCarPriceSpider = XcarDealerCarPriceSpider()
DealerSpider = XcarDealerSpider()
DealerAboutSpider = XcarDealerAboutSpider()
DealerActivitySpider = XcarDealerActivitySpider()
DealerCommentSpider = XcarDealerCommentSpider()
DealerDianPingSpider = XcarDealerDianPingSpider()
DealerIndexSpider = XcarDealerIndexSpider()
DealerNewsSpider = XcarDealerNewsSpider()
DealerPictureSpider = XcarDealerPictureSpider()
DealerPriceSpider = XcarDealerPriceSpider()
DriveSpider = XcarDriveSpider()
ForumSpider = XcarForumSpider()
GreenSpider = XcarGreenSpider()
GuideSpider = XcarGuideSpider()
HelpSpider = XcarHelpSpider()
IndexSpider = XcarIndexSpider()
InstituteSpider = XcarInstituteSpider()
KoubeiSpider = XcarKoubeiSpider()
NewCarSpider = XcarNewCarSpider()
PhotoSpider = XcarPhotoSpider()
BrandPictureSpider = XcarBrandPictureSpider()
QiuGouSpider = XcarQiuGouSpider()
SelectedSpider = XcarSelectedSpider()
SUVSpider = XcarSUVSpider()
TechSpider = XcarTechSpider()
UsedcarSpider = XcarUsedcarSpider()
BrandVideoSpider = XcarBrandVideoSpider()
WikiSpider = XcarWikiSpider()
XviewSpider = XcarXviewSpider()
BrandyangcheSpider = XcarBrandyangcheSpider()


connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
db = connection[settings['MONGODB_DB']]

configure_logging(settings)
runner = CrawlerRunner(settings)


@defer.inlineCallbacks
def crawl():
    # yield runner.crawl(BrandlistSpider)
    # yield runner.crawl(DealerSpider)
    # yield runner.crawl(IndexSpider)
    # yield runner.crawl(BrandBaojiaSpider)
    # yield runner.crawl(BrandConfigSpider)
    # yield runner.crawl(BrandinfoSpider)
    # yield runner.crawl(BrandvehicleSpider)
    yield runner.crawl(BrandPictureSpider)
    # yield runner.crawl(KoubeiSpider)
    # yield runner.crawl(BrandyangcheSpider)
    # yield runner.crawl(BrandVideoSpider)
    # yield runner.crawl(UsedcarSpider)
    # yield runner.crawl(DealerCarPriceSpider)
    # yield runner.crawl(DealerAboutSpider)
    # yield runner.crawl(DealerActivitySpider)
    # yield runner.crawl(DealerCommentSpider)
    # yield runner.crawl(DealerDianPingSpider)
    # yield runner.crawl(DealerIndexSpider)
    yield runner.crawl(DealerNewsSpider)
    yield runner.crawl(DealerPictureSpider)
    yield runner.crawl(DealerPriceSpider)
    yield runner.crawl(BookSpider)
    yield runner.crawl(DriveSpider)
    yield runner.crawl(GreenSpider)
    yield runner.crawl(GuideSpider)
    yield runner.crawl(HelpSpider)
    yield runner.crawl(InstituteSpider)
    yield runner.crawl(NewCarSpider)
    yield runner.crawl(QiuGouSpider)
    # yield runner.crawl(SelectedSpider)
    yield runner.crawl(SUVSpider)
    yield runner.crawl(TechSpider)
    yield runner.crawl(WikiSpider)
    yield runner.crawl(XviewSpider)
    # yield runner.crawl(PhotoSpider)
    # yield runner.crawl(ForumSpider)
    # yield runner.crawl(ActivitySpider)

    reactor.stop()


crawl()
reactor.run()  # the script will block here until the last crawl call is finished