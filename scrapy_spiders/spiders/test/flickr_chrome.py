# -*- coding: utf-8 -*-
import json
import logging
import re

from scrapy import Request, Spider
from scrapy.utils.project import get_project_settings

from scrapy_common.exceptions import FieldError
# import scrapy_redis.dupefilter.RFPDupeFilter
from scrapy_redis.spiders import RedisSpider
from scrapy_spiders.items import ImgItem

logger = logging.getLogger(__name__)


class FlickrSpider(RedisSpider):
# class FlickrSpider(Spider):
    #     RFPDupeFilter

    custom_settings = {

        'DOWNLOADER_MIDDLEWARES': {
            'scrapy_spiders.downloadmiddlewares.flickr_selenium.SeleniumMiddleWare': 500
        }
    }

    name = 'flickr_chrome'
    api = 'https://api.flickr.com/services/rest?sort=relevance&parse_tags=1&content_type=7&extras=can_comment%2Ccount_comments%2Ccount_faves%2Cdescription%2Cisfavorite%2Clicense%2Cmedia%2Cneeds_interstitial%2Cowner_name%2Cpath_alias%2Crealname%2Crotation%2Curl_c%2Curl_l%2Curl_m%2Curl_n%2Curl_q%2Curl_s%2Curl_sq%2Curl_t%2Curl_z&per_page=50&page={page}&lang=zh-Hant-HK&text={text}&viewerNSID=&method=flickr.photos.search&csrf=&api_key={api_key}&format=json&hermes=1&hermesClient=1&reqId=8ce77476&nojsoncallback=1'

    ima_url = 'https://farm{farm_id}.staticflickr.com/{server_id}/{id}_{secret}_m.jpg'

    start_urls = ['https://www.flickr.com/']

    def __init__(self, *args, **kwargs):
        settings = get_project_settings()
        self.flickr_api_key = settings.get('FLICKR_API_KEY', None)
        if not self.flickr_api_key:
            raise FieldError('请在配置文件中正确配置FLICKR_API_KEY字段')

        self.page = 3
        self.text = 'knife'
        super().__init__(*args, **kwargs)


    def start_requests(self):
        yield Request('https://www.flickr.com/', dont_filter=True)

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
            **kwargs, dont_filter=True)

    def parse(self, response):
        request = response.request
        meta = request.meta
        yield Request(url=self.api.format(api_key=meta.get('key'), page=10, text='knife'),
                      cookies=request.cookies, callback=self.parse_json, dont_filter=True)

    def parse_json(self, response):
        json_content = json.loads(response.text)
        print(json_content)
        # print('ok')

        photos = json_content.get('photos', {}).get('photo', {})
        for photo in photos:
            img_url = photo.get('url_l')
            if not img_url:
                continue

            item = ImgItem()

            item['url'] = img_url
            item['site'] = 'flickr'
            item['_id'] = photo.get('id')
            if not item['url']:
                continue

            yield item



