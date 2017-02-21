# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from scrapy.conf import settings
from scrapy import log
import functools
from scrapy.exceptions import DropItem


def check_spider_pipeline(process_item_method):

    """
    此方法用于检验不同的spider所对应处理item的pipeline
    :param process_item_method:
    :return:
    """
    @functools.wraps(process_item_method)
    def wrapper(self, item, spider):

        # message template for debugging
        msg = '%%s %s pipeline step' % (self.__class__.__name__,)

        # if class is in the spider's pipeline, then use the
        # process_item method normally.
        if self.__class__ in spider.pipeline:
            # print(spider.pipeline)
            spider.log(msg % 'executing', level=log.DEBUG)
            return process_item_method(self, item, spider)

        # otherwise, just return the untouched item (skip this step in
        # the pipeline)
        else:
            # spider.log(msg % 'skipping', level=log.DEBUG)
            return item

    return wrapper

class XcarActivityPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db['Activity']

    @check_spider_pipeline
    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item

class XcarBookPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db['Book']

    @check_spider_pipeline
    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item

class XcarBrandBaojiaPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db['BrandBaojia']

    @check_spider_pipeline
    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item

class XcarBrandConfigPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db['BrandConfig']

    @check_spider_pipeline
    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item

class XcarBrandInfoPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db['BrandInfo']

    @check_spider_pipeline
    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item

class XcarBrandVehiclePipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db['BrandVehicle']

    @check_spider_pipeline
    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item

class XcarCarPricePipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db['CarPrice']

    @check_spider_pipeline
    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item

class XcarDealerAboutPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db['DealerAbout']

    @check_spider_pipeline
    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item

class XcarDealerActivityPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db['DealerActivity']

    @check_spider_pipeline
    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item

class XcarDealerCommentPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db['DealerComment']

    @check_spider_pipeline
    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item

class XcarDealerDianpingPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db['DealerDianping']

    @check_spider_pipeline
    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item

class XcarDealerIndexPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db['DealerIndex']

    @check_spider_pipeline
    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item

class XcarDealerNewsPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db['DealerNews']

    @check_spider_pipeline
    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item

class XcarDealerPicturePipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db['DealerPic']

    @check_spider_pipeline
    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item

class XcarDealerPricePipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db['DealerPrice']

    @check_spider_pipeline
    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item

class XcarDrivePipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db['Drive']

    @check_spider_pipeline
    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item

class XcarGreenPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db['Green']

    @check_spider_pipeline
    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item

class XcarGuidePipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db['Guide']

    @check_spider_pipeline
    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item

class XcarHelpPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db['Help']

    @check_spider_pipeline
    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item

class XcarInstitutePipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db['Institute']

    @check_spider_pipeline
    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item

class XcarNewCarPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db['Newcar']

    @check_spider_pipeline
    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item

class XcarPhotoPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db['Photo']

    @check_spider_pipeline
    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item

class XcarPicturePipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db['Picture']

    @check_spider_pipeline
    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item

class XcarQiugouPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db['Qiugou']

    @check_spider_pipeline
    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item

class XcarSelectedPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db['Selected']

    @check_spider_pipeline
    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item

class XcarSuvPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db['SUV']

    @check_spider_pipeline
    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item

class XcarTechPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db['Technology']

    @check_spider_pipeline
    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item

class XcarUsedCarPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db['UsedCar']

    @check_spider_pipeline
    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item

class XcarVideoPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db['Video']

    @check_spider_pipeline
    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item

class XcarYangchePipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db['Yangche']

    @check_spider_pipeline
    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item

class XcarWikiPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db['Wiki']

    @check_spider_pipeline
    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item

class XcarViewPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db['View']

    @check_spider_pipeline
    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item

class XcarForumPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db['Forum']

    @check_spider_pipeline
    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item

class XcarKoubeiPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db['Koubei']

    @check_spider_pipeline
    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item

class XcarIndexPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db['Index']

    @check_spider_pipeline
    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item