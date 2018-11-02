from scrapy.utils.misc import load_object
from scrapy.utils.project import get_project_settings

from scrapy_common.utils import get_spider_name
from scrapy_redis.scheduler import Scheduler


class SchedulerMgr(Scheduler):
    # 调度类
    queue_cls = 'scrapy_redis.queue.PriorityQueue'

    def __init__(self, *args, **kwargs):
        self.queue = None
        self.spider = None
        self.df = None
        super(SchedulerMgr, self).__init__(*args, **kwargs)

    def scheduler_request(self, spider_name, *args, **kwargs):
        """

        :param spider_name: 爬虫名字
        :param args:
        :param kwargs: scrapy.Request的关键字参数
        :return:
        """
        spider = get_spider_name(spider_name)
        settings = get_project_settings()

        # redis队列初始化
        self.queue = load_object(self.queue_cls)(
            server=self.server,
            spider=spider,
            key=self.queue_key % {'spider': spider.name},
            serializer=self.serializer,
        )

        # 初始化去重队列
        spider.settings = settings

        self.spider = spider

        self.df = load_object(self.dupefilter_cls).from_spider(spider)

        self.enqueue_request(spider.create_request(*args, **kwargs))


    @classmethod
    def from_settings(cls):
        """

        :param spider:通过spider的名字进行spider任务的调度
        :return:
        """

        settings = get_project_settings()

        # 基础功能的初始化
        instance = super().from_settings(settings)

        return instance


scheduler_instance = SchedulerMgr.from_settings()
