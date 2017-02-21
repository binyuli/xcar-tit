import pymongo
from scrapy.conf import settings

connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
db = connection[settings['MONGODB_DB']]

def save_brandlist(result):
    connection=db['Brand']
    connection.save(result)

def save_dealerlist(result):
    connection=db['Dealer']
    connection.save(result)

def get_baojia_url():
    connection = db['Brand']
    starturs = list()
    for item in connection.find():
        brand=dict()
        if 'baojia_url' in item.keys() and 'cid' in item.keys():
            brand['baojia_url']=item['baojia_url']
            brand['cid']=item['cid']
            starturs.append(brand)
    return starturs

def get_config_url():
    connection = db['Brand']
    starturs = set()
    for brand in connection.find():
        if 'config_url' in brand.keys():
            starturs.add(brand['config_url'])
    return starturs

def get_pic_url():
    connection = db['Brand']
    starturs = set()
    for brand in connection.find():
        if 'pic_url' in brand.keys():
            starturs.add(brand['pic_url'])
    return starturs

def get_video_url():
    connection = db['Brand']
    starturs = set()
    for brand in connection.find():
        if 'video_url' in brand.keys():
            starturs.add(brand['video_url'])
    return starturs

def get_yangche_url():
    connection = db['Brand']
    starturs = set()
    for brand in connection.find():
        if 'baoyang_url' in brand.keys():
            starturs.add(brand['baoyang_url'])
    return starturs

def get_article_url():
    connection = db['Brand']
    starturs = set()
    for brand in connection.find():
        if 'article_url' in brand.keys():
            starturs.add(brand['article_url'])
    return starturs

def get_vehicle_url():
    connection = db['Brand']
    starturs = set()
    for brand in connection.find():
        if 'vehicle_url' in brand.keys():
            starturs.add(brand['vehicle_url'])
    return starturs

def get_dealerabout_url():
    connection = db['Dealer']
    starturs = set()
    for brand in connection.find():
        if 'about_url' in brand.keys():
            starturs.add(brand['about_url'])
    return starturs

def get_dealeractivity_url():
    connection = db['Dealer']
    starturs = set()
    for brand in connection.find():
        if 'activity_url' in brand.keys():
            starturs.add(brand['activity_url'])
    return starturs

def get_dealercomment_url():
    connection = db['Dealer']
    starturs = set()
    for brand in connection.find():
        if 'activity_url' in brand.keys():
            starturs.add(brand['activity_url'])
    return starturs

def get_dealerdianping_url():
    connection = db['Dealer']
    starturs = set()
    for brand in connection.find():
        if 'dianping_url' in brand.keys():
            starturs.add(brand['dianping_url'])
    return starturs

def get_dealernews_url():
    connection = db['Dealer']
    starturs = set()
    for brand in connection.find():
        if 'news_url' in brand.keys():
            starturs.add(brand['news_url'])
    return starturs

def get_dealerpic_url():
    connection = db['Dealer']
    starturs = set()
    for brand in connection.find():
        if 'photo_url' in brand.keys():
            starturs.add(brand['photo_url'])
    return starturs

def get_dealerprice_url():
    connection = db['Dealer']
    starturs = set()
    for brand in connection.find():
        if 'price_url' in brand.keys():
            starturs.add(brand['price_url'])
    return starturs




