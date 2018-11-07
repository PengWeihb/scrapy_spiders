# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class ScrapySpidersItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class QuoteItem(scrapy.Item):
    text = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()


class ChinaItem(scrapy.Item):
    title = Field()
    url = Field()
    text = Field()
    datetime = Field()
    source = Field()
    website = Field()


# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html


import scrapy
from scrapy import Field


class AiscrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class DoubanImgsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # image_urls = Field()
    # images = Field()
    # image_paths = Field()
    pass


class ImgItem(scrapy.Item):
    url = Field()
    site = Field()
    text = Field()
    _id = Field()



