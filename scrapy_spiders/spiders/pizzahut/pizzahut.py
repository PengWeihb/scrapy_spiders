# -*- coding: utf-8 -*-
import logging
import urllib

from scrapy import Spider, Request, Item, Field
from scrapy.dupefilter import RFPDupeFilter
from scrapy.utils.response import get_base_url

from scrapy_spiders.items import QuoteItem

logger = logging.getLogger(__name__)


class PizzahutItem(Item):
    locations = Field()
    phone = Field()
    longitude_latitude = Field()


class PizzahutSpider(Spider):
    # name = 'pizzahut'

    name = 'pizzahut'
    allowed_domains = ['www.pizzahut.com.cn']
    start_urls = ['http://www.pizzahut.com.cn/StoreList']

    def parse(self, response):
        citys = response.xpath('//div[@class="l_to_chose"]')

        for city in citys:
            letters = city.xpath('.//div/a/text()').extract()
            for letter in letters:
                print(letter)
                yield Request(url=self.start_urls[0], callback=self.parse_html,
                              cookies={'iplocation': urllib.parse.quote(
                                  '{0}|0|0'.format(letter))}, dont_filter=True)
                

    def parse_html(self, response):

        values = response.xpath('//div/input[@type="hidden"]/@value').extract()



        item = PizzahutItem()

        for value in values:
            value = value.split('|')
            item['longitude_latitude'] = value[0]
            item['phone'] = value[3]
            item['locations'] = value[1] + value[2]

            print(values)

            yield item

        # temp = response.xpath('//*[@id="mCSB_1_container"]/ul/li[1]/div[2]/p[2]')
        # logger.info(response.text)
