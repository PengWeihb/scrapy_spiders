# -*-coding:utf-8 -*-
# 通过调用命令行进行调试

# 调用execute这个函数可调用scrapy脚本

# 设置工程命令

# 设置工程路径，在cmd 命令更改路径而执行scrapy命令调试
# 获取main文件的父目录，os.path.abspath(__file__) 为__file__文件目录

# sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# execute(["scrapy", "crawl", "china"])
# execute("scrapy crawl china")


from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from scrapy_spiders.spiders.common.configs.utils import get_config

from scrapy.cmdline import execute


def run():
    name = 'china'
    custom_settings = get_config(name)
    spider = custom_settings.get('spider', 'universal')
    project_settings = get_project_settings()
    settings = dict(project_settings.copy())
    settings.update(custom_settings.get('settings'))
    process = CrawlerProcess(settings)
    process.crawl(spider, **{'name': name})
    process.start()


if __name__ == '__main__':
    # run()

    execute(["scrapy", "crawl", "flickr", "-a", "close='a'"])

    # execute(["scrapy", "crawl", "flickr_chrome"])
