


class MyBaseError(Exception):
    message = ''
    def __init__(self, info):
        super().__init__(self)
        self.info = info if info else self.message

    def __str__(self):
        return self.info


class FieldError(MyBaseError):
    """
    如果读取scrapy配置文件中的字段错误，抛出改错误

    """
    message = 'setting field error'


class ParamsError(MyBaseError):
    """
    如果给爬虫的参数发生错误，抛出该错误
    """
    message = 'parameters error'



