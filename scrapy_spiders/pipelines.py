# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline

from scrapy_redis import get_redis_from_settings


class ScrapySpidersPipeline(object):

    def process_item(self, item, spider):
        return item


class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(mongo_uri=crawler.settings.get('MONGO_URI'),
                   mongo_db=crawler.settings.get('MONGO_DB'))

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        name = item.__class__.__name__
        self.db[name].insert(dict(item))
        return item

    def close_spier(self, spider):
        self.client.close()


class AiscrapyPipeline(object):
    def process_item(self, item, spider):
        return item


class ImagePipeline(ImagesPipeline):
    redis_key = 'image:'

    def __init__(self, *args, **kwargs):
        super(ImagePipeline, self).__init__(*args, **kwargs)

        settings = kwargs.get('settings')
        self.server = get_redis_from_settings(settings)
        self.key = 'image_dupefilter'

    # @classmethod
    # def from_settings(cls, settings):
    #     print('asdf')

    # def file_path(self, request, response=None, info=None):
    #     """
    #     返回文件名
    #     :param request:
    #     :param response:
    #     :param info:
    #     :return:
    #     """
    #
    #     # print(info.get('downloaded'))
    #     path = super(ImagePipeline, self).file_path(request, response=None,
    #                                                 info=None)
    #
    #     path = path.replace('full/', '')
    #
    #     return path

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]

        if not image_paths:
            raise DropItem('Image Downloaded Failed')

        return item

    def get_media_requests(self, item, info):

        if self.dupefilter(item, info):
            yield Request(item['url'])

    def dupefilter(self, item, info):
        added = self.server.sadd(self.redis_key + item['site'] + '_dupefilter',
                                 item['_id'])
        return added
