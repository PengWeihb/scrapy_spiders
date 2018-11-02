# -*- coding: utf-8 -*-
import json
import logging
from json import JSONDecodeError

import scrapy
from scrapy import Request
from scrapy.utils.project import get_project_settings
from scrapy_redis.dupefilter import RFPDupeFilter
from scrapy_redis.spiders import RedisSpider

# from AiScrapy.items import FlickrItem, ImgItem
from scrapy_common.exceptions import ParamsError, FieldError
from scrapy_spiders.items import ImgItem

logger = logging.getLogger(__name__)


# RedisSpider

class BaiduImgSpider(RedisSpider):
    # class BaiduImgSpider(scrapy.Spider):

    name = 'baidu_img'

    # pn是30的倍速
    api = 'https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord={text}&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&word=knife&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&expermode=&pn={page}&rn=3&gsm=78&1540431170467='

    def __init__(self, *args, **kwargs):
        settings = get_project_settings()
        self.flickr_api_key = settings.get('FLICKR_API_KEY', None)
        if not self.flickr_api_key:
            raise FieldError('请在配置文件中正确配置FLICKR_API_KEY字段')
        self.page = 3
        self.text = 'knife'
        self.start_urls = [
            self.api.format(page=self.page * 30,
                            text=self.text)]
        # print('sadf', *args, **kwargs)
        super().__init__(*args, **kwargs)

    # @classmethod
    # def schedule(cls, *args, **kwargs):
    #     meta = kwargs.get('meta')
    #     page = meta.get('page')
    #     text = meta.get('text')
    #     return Request(
    #         cls.api.format(page=int(page) * 30, text=text),
    #         **kwargs)

    @classmethod
    def create_request(cls, *args, **kwargs):
        meta = kwargs.get('meta')
        page = meta.get('page')
        text = meta.get('text')
        return Request(
            cls.api.format(page=int(page) * 30, text=text),
            **kwargs)

    def parse(self, response):
        try:
            json_content = json.loads(response.body.decode())
            datas = json_content.get('data', {})
            for data in datas:
                img_item = ImgItem()
                img_url = data.get('thumbURL')
                if not img_url:
                    continue
                img_item['url'] = img_url
                img_item['site'] = 'baidu'
                yield img_item


        except JSONDecodeError as e:
            logger.error(e)
        finally:
            pass




    # def parse_two(self, response):
    #     print(self.page)
    #     print('*************')





