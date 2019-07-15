from selenium import webdriver
import time
from scrapy.http import HtmlResponse

class TenxunSpiderMiddleware(object):
    def __init__(self):
        self.driver = webdriver.PhantomJS(executable_path=r'C:\Users\Administrator\Desktop\phantomjs-2.1.1-windows\bin\phantomjs.exe')

    def process_request(self, request, spider):
        if request.meta.get('phantomjs'):

            self.driver.get(request.url)
            time.sleep(2)
            html = self.driver.page_source
            print(html)
            return HtmlResponse(url = request.url, body=html, encoding='utf-8', request= request)





