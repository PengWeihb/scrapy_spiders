from scrapy_common.scheduler_mgr import scheduler_instance


def baidu_img_schedule(page=100):
    for i in range(1, page):
        scheduler_instance.scheduler_request('baidu_img',
                                             **{'dont_filter': True,
                                                'meta': {'page': i,
                                                         'text': 'knife'}})


def flickr_img_schedule():
    scheduler_instance.scheduler_request('flickr',
                                         **{'dont_filter': True,
                                            'meta': {'page': 1,
                                                     'text': 'knife'}})


if __name__ == '__main__':

    # baidu_img_schedule(100)

    flickr_img_schedule()
