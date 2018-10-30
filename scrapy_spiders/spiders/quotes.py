# -*- coding: utf-8 -*-
import scrapy
from scrapy.utils.response import get_base_url

from scrapy_spiders.items import QuoteItem


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        # 采用css选择器
        quotes = response.css('.text')
        for quote in quotes:
            item = QuoteItem()
            item['text'] = quote.css('.text::text').extract_first()
            item['author'] = quote.css('.author::text').extract_first()
            item['tags'] = quote.css('.tags .tag::text').extract()
            yield item
        next_page = response.css('.paper .next a::attr(href)').extract_first()
        url = response.urljoin(next_page)
        print(get_base_url(response))
        yield scrapy.Request(url=url, callback=self.parse)


# 可以直接通过
# scrapy crawl quotes -o quotes.json
# scrapy crawl quotes -o quotes.jl  (jl = jsonline 或者 .cvs .xml等)




