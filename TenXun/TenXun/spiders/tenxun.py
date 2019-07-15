# -*- coding: utf-8 -*-
import scrapy
import json
from ..items import TenxunItem
from lxml import etree
import time

class TenxunSpider(scrapy.Spider):
    name = 'tenxun'
    allowed_domains = ['careers.tencent.com']
    start_urls = []
    for i in range(1,6):
        url = f'https://careers.tencent.com/tencentcareer/api/post/Query?countryId=&cityId=&bgIds=&productId=&categoryId=&parentCategoryId=&attrId=&keyword=python&pageIndex={i}&pageSize=10&language=zh-cn&area=cn'
        start_urls.append(url)
    def parse(self, response):
        html = response.body.decode('utf-8')
        html = json.loads(html)
        all = html.get('Data').get('Posts')
        for list in all:
            item = TenxunItem()
            title = list.get('RecruitPostName')
            address_s = list.get('CountryName')
            address_d = list.get('LocationName')
            address = address_d+','+address_s
            class_s = list.get('CategoryName')
            name = list.get('BGName')
            time = list.get('LastUpdateTime')
            miaos = list.get('Responsibility')
            miao = miaos.replace('\n','').replace('\r','')

            url = list.get('PostId')
            url2= 'https://careers.tencent.com/jobdesc.html?postId='
            postURL = url2+url

            print(postURL)

            item['title'] = title
            item['name'] = name
            item['address'] = address
            item['class_s'] = class_s
            item['time'] = time
            item['miao'] = miao
            item['postURL'] = postURL

            #封装二次请求
            yield scrapy.Request(postURL,callback=self.parse_detail,meta = {'data':item,'phantomjs':True},dont_filter=True)


    def parse_detail(self,response):
        print('======================================')
        item = response.request.meta['data']
        #提取工作
        content =response.body.decode('utf-8')
        tree = etree.HTML(content)
        jobskill = tree.xpath('//div[@class="requirement work-module"]/div/ul/li/text()')
        if jobskill:
             jobskill=''.join(jobskill)
            ##提取工作要求:
             item['jobskill'] =jobskill
        else:
             item['jobskill'] = 'None'
        yield item



