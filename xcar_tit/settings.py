# -*- coding: utf-8 -*-

# Scrapy settings for xcar_tit project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'xcar_tit'

SPIDER_MODULES = ['xcar_tit.spiders']
NEWSPIDER_MODULE = 'xcar_tit.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'xcar_tit (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'xcar_tit.middlewares.MyCustomSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'xcar_tit.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'xcar_tit.pipelines.SomePipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'



SCHEDULER = "scrapy_redis.scheduler.Scheduler"
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
# Don't cleanup redis queues, allows to pause/resume crawls.
SCHEDULER_PERSIST = True
# REDIS_START_URLS_BATCH_SIZE = 1000000


MONGODB_SERVER = "localhost"
# MONGODB_SERVER = "192.168.7.127"
MONGODB_PORT = 27017
MONGODB_DB = "Xcar_tit"

ITEM_PIPELINES = {
    'xcar_tit.pipelines.XcarActivityPipeline': 300,
    'xcar_tit.pipelines.XcarBookPipeline': 301,
    'xcar_tit.pipelines.XcarBrandBaojiaPipeline': 302,
    'xcar_tit.pipelines.XcarBrandConfigPipeline': 303,
    'xcar_tit.pipelines.XcarBrandInfoPipeline': 304,
    'xcar_tit.pipelines.XcarBrandVehiclePipeline': 305,
    'xcar_tit.pipelines.XcarCarPricePipeline': 306,
    'xcar_tit.pipelines.XcarDealerAboutPipeline': 307,
    'xcar_tit.pipelines.XcarDealerActivityPipeline': 308,
    'xcar_tit.pipelines.XcarDealerCommentPipeline': 309,
    'xcar_tit.pipelines.XcarDealerDianpingPipeline': 310,
    'xcar_tit.pipelines.XcarDealerIndexPipeline': 311,
    'xcar_tit.pipelines.XcarDealerNewsPipeline': 312,
    'xcar_tit.pipelines.XcarDealerPicturePipeline': 313,
    'xcar_tit.pipelines.XcarDealerPricePipeline': 314,
    'xcar_tit.pipelines.XcarDrivePipeline': 315,
    'xcar_tit.pipelines.XcarGreenPipeline': 316,
    'xcar_tit.pipelines.XcarGuidePipeline': 317,
    'xcar_tit.pipelines.XcarHelpPipeline': 318,
    'xcar_tit.pipelines.XcarInstitutePipeline': 319,
    'xcar_tit.pipelines.XcarNewCarPipeline': 320,
    'xcar_tit.pipelines.XcarPhotoPipeline': 321,
    'xcar_tit.pipelines.XcarPicturePipeline': 322,
    'xcar_tit.pipelines.XcarQiugouPipeline': 323,
    'xcar_tit.pipelines.XcarSelectedPipeline': 324,
    'xcar_tit.pipelines.XcarSuvPipeline': 325,
    'xcar_tit.pipelines.XcarTechPipeline': 326,
    'xcar_tit.pipelines.XcarUsedCarPipeline': 327,
    'xcar_tit.pipelines.XcarVideoPipeline': 328,
    'xcar_tit.pipelines.XcarYangchePipeline': 329,
    'xcar_tit.pipelines.XcarWikiPipeline': 330,
    'xcar_tit.pipelines.XcarViewPipeline': 331,
    'xcar_tit.pipelines.XcarIndexPipeline': 332,


}


REDIS_HOST = 'localhost'
# REDIS_HOST = '192.168.7.126'
REDIS_PORT = 6379

FILTER_MOD = 'Update'
START_DATE = '2014-1-1'
