# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from scrapy_spiders.items import ChinaItem
from scrapy_spiders.spiders.common.configs.item_loader import ChinaLoader


class ChinaSpider(CrawlSpider):
    name = 'china'
    allowed_domains = ['tech.china.com']
    start_urls = ['http://tech.china.com/articles/']

    # allow 允许的规则，正则表示
    # restrict_xpaths 在指定的区域提取链接
    rules = (
        Rule(LinkExtractor(allow='article/.*\.html',
                           restrict_xpaths='//div[@class="conR"]/h2/a'),
             callback='parse_item'),
        Rule(LinkExtractor(
            restrict_xpaths='//div[@id="pageStyle"]//a[contains(., "下一页")]'))
    )

    def __init__(self):
        print(self.start_urls)

    def parse_item(self, response):
        loader = ChinaLoader(item=ChinaItem(), response=response)
        loader.add_xpath('title', '//h1[@id="chan_newsTitle"]/text()')
        loader.add_value('url', response.url)
        loader.add_xpath('text', '//div[@id="chan_newsDetail"]//text()')
        loader.add_xpath('datetime', '//div[@id="chan_newsInfo"]/text()',
                         re='(\d+-\d+-\d+\s\d+:\d+:\d+)')
        loader.add_xpath('source', '//div[@id="chan_newsInfo"]/text()',
                         re='来源：(.*)')
        loader.add_value('website', '中华网')
        yield loader.load_item()
