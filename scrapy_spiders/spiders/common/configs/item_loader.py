from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Compose, Join


class NewsLoader(ItemLoader):
    default_output_processor = TakeFirst()


class ChinaLoader(NewsLoader):
    text_out = Compose(Join(), lambda s: s.strip())
    source_out = Compose(Join(), lambda s: s.strip())