import logging
import re
import time

from scrapy.http import Response
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

logger = logging.getLogger(__name__)


class SeleniumMiddleWare(object):

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)
        self.url = 'https://www.flickr.com/'

    def process_request(self, request, spider):
        try:
            if request.cookies:
                return
            self.driver.get('https://www.flickr.com/')
            # time.sleep(2)

            print('*****', self.driver.get_cookies())
            request.cookies = self.driver.get_cookies()
            content = self.driver.page_source
            pattern = re.compile(r'site_key = "(.*?)"')
            key = pattern.findall(content)[0]
            request.meta['key'] = key
            return Response(url=self.url, request=request)
        except Exception as e:
            logger.error(e)
        finally:
            pass


    def process_exception(self, request, exception, spider):
        print('***********************')

    def __del__(self):
        self.driver.close()
