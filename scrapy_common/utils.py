from scrapy.spiderloader import SpiderLoader
from scrapy.utils.project import get_project_settings


def get_spider_name(name):
    """
    通过name得到spider的实列
    :param name: 爬虫的name
    :return:
    """
    settings = get_project_settings()
    loader = SpiderLoader.from_settings(settings)
    spider = loader.load(name)
    return spider






