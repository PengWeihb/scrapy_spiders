# -*- coding: utf-8 -*-
import logging

from scrapy import Request, Spider
from scrapy.exceptions import CloseSpider
from scrapy.utils.project import get_project_settings

from scrapy_common.exceptions import FieldError
# import scrapy_redis.dupefilter.RFPDupeFilter
from scrapy_redis.spiders import RedisSpider
from scrapy_spiders.items import ImgItem

logger = logging.getLogger(__name__)



class FlickrSpider(RedisSpider):
# class FlickrSpider(Spider):
    #     RFPDupeFilter

    name = 'flickr'
    # allowed_domains = ['quotes.toscrape.com']

    api = 'https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key={flickr_api_key}&text={text}&page={page}&sort=relevance&extras=url_o,url_l'

    ima_url = 'https://farm{farm_id}.staticflickr.com/{server_id}/{id}_{secret}_m.jpg'

    def __init__(self, *args, **kwargs):
        # super(FlickrSpider, self).__init__(*args, **kwargs)
        super().__init__(*args, **kwargs)
        settings = get_project_settings()
        self.flickr_api_key = settings.get('FLICKR_API_KEY', None)
        if not self.flickr_api_key:
            raise FieldError('请在配置文件中正确配置FLICKR_API_KEY字段')

        self.page = 3
        self.text = 'knife'
        self.start_urls = [
            self.api.format(page=self.page, flickr_api_key=self.flickr_api_key,
                            text=self.text)]

        # if kwargs.get('close'):
        # raise CloseSpider


    # @classmethod
    # def from_crawler(cls, crawler, *args, **kwargs):
    #     obj = super().from_crawler(crawler, *args, kwargs)
    #     return obj



    @classmethod
    def create_request(cls, *args, **kwargs):
        meta = kwargs.get('meta')
        page = meta.get('page')
        text = meta.get('text')
        settings = get_project_settings()
        flickr_api_key = settings.get('FLICKR_API_KEY', None)
        return Request(
            cls.api.format(page=page, text=text,
                           flickr_api_key=flickr_api_key),
            **kwargs)

    def parse(self, response):
        meta = response.meta
        print('爬取成功', meta)
        print(type(response.body))
        # json_content = json.loads(response.body.decode())
        # print(response.body.decode())
        photos = response.xpath('//photo')
        for photo in photos:

            item = ImgItem()
            item['url'] = photo.xpath('./@url_o').extract_first()
            if not item['url']:
                item['url'] = photo.xpath('./@url_l').extract_first()
            item['site'] = 'flickr'
            item['_id'] = photo.xpath('./@id').extract_first()
            if not item['url']:
                continue

            yield item

        page = int(response.xpath('//photos/@page').extract_first())
        pages = int(response.xpath('//photos/@pages').extract_first())

        print('page = ', page, pages)

        if page == 1:
            for i in range(2, 10):
                yield self.create_request(
                    **{'dont_filter': True,
                       'meta': {'page': i, 'text': 'knife'}})

    # def parse_two(self):
    #     print('*************')
