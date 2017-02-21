# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field

class XcarTitItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class XcarActivityItem(Item):
    tit=Field()
    url=Field()
    address = Field()
    category = Field()

class XcarBookItem(Item):
    tit=Field()
    url=Field()
    address = Field()
    category = Field()

class XcarBrandbaojiaUrlItem(Item):
    tit=Field()
    url=Field()
    address = Field()
    category = Field()

class XcarBrandConfigUrlItem(Item):
    tit=Field()
    url=Field()
    address = Field()
    category = Field()

class XcarBrandvehicleUrlItem(Item):
    tit=Field()
    url=Field()
    address = Field()
    category = Field()

class XcarBrandinfoUrlItem(Item):
    tit=Field()
    url=Field()
    address = Field()
    category = Field()

class XcarDealerCarPriceItem(Item):
    tit=Field()
    url=Field()
    address = Field()
    category = Field()

class XcarDealerAboutItem(Item):
    tit=Field()
    url=Field()
    address = Field()
    category = Field()

class XcarDealerActivityItem(Item):
    tit=Field()
    url=Field()
    address = Field()
    category = Field()

class XcarDealerCommentItem(Item):
    tit=Field()
    url=Field()
    address = Field()
    category = Field()

class XcarDealerDianPingItem(Item):
    tit=Field()
    url=Field()
    address = Field()
    category = Field()

class XcarDealerNewsItem(Item):
    tit=Field()
    url=Field()
    address = Field()
    category = Field()

class XcarDealerPictureItem(Item):
    tit=Field()
    url=Field()
    address = Field()
    category = Field()

class XcarDealerPriceItem(Item):
    tit=Field()
    url=Field()
    category = Field()

class XcarDealerIndexItem(Item):
    tit=Field()
    url=Field()
    category = Field()

class XcarDriveItem(Item):
    tit=Field()
    url=Field()
    address = Field()
    category = Field()

class XcarGreenItem(Item):
    tit=Field()
    url=Field()
    address = Field()
    category = Field()

class XcarGuideItem(Item):
    tit=Field()
    url=Field()
    address = Field()
    category = Field()

class XcarHelpItem(Item):
    tit=Field()
    url=Field()
    address = Field()
    category = Field()

class XcarInstituteItem(Item):
    tit=Field()
    url=Field()
    address = Field()
    category = Field()

class XcarNewCarUrlItem(Item):
    tit=Field()
    url=Field()
    address = Field()
    category = Field()

class XcarPhotoItem(Item):
    tit=Field()
    url=Field()
    address = Field()
    category = Field()

class XcarBrandpictureUrlItem(Item):
    tit=Field()
    url=Field()
    address = Field()
    category = Field()

class XcarDealerQiuGouItem(Item):
    tit=Field()
    url=Field()
    address = Field()
    category = Field()

class XcarSelectedItem(Item):
    tit=Field()
    url=Field()
    address = Field()
    category = Field()

class XcarSUVItem(Item):
    tit=Field()
    url=Field()
    address = Field()
    category = Field()

class XcarTechItem(Item):
    tit=Field()
    url=Field()
    address = Field()
    category = Field()

class XcarUsedCarItem(Item):
    tit=Field()
    url=Field()
    address = Field()
    category = Field()

class XcarBrandvideoUrlItem(Item):
    tit=Field()
    url=Field()
    address = Field()
    category = Field()

class XcarBrandyangchelItem(Item):
    tit=Field()
    url=Field()
    address = Field()
    category = Field()

class XcarWikiItem(Item):
    tit=Field()
    url=Field()
    address = Field()
    category = Field()

class XcarXviewItem(Item):
    tit=Field()
    url=Field()
    address = Field()
    category = Field()

class XcarIndexUrlItem(Item):
    title=Field()
    url=Field()

class XcarBrandkoubeiUrlItem(Item):
    tit=Field()
    url=Field()
    address = Field()
    category = Field()

class XcarForumItem(Item):
    tit=Field()
    url=Field()
    address = Field()
    category = Field()









