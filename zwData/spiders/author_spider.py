import os
import re
import uuid
import scrapy
from zwData.items import AuthorItem
from zwData.spiders.util import UtilClass


class AuthorSpider(scrapy.Spider):
    name = 'author'
    allowed_domains = ['kns.cnki.net']

    # 获取setting中的年份和是否在解析失败的链接内容
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = cls(crawler.settings, *args, **kwargs)
        spider._set_crawler(crawler)
        return spider

    def __init__(self, settings, *args, **kwargs):
        super(AuthorSpider, self).__init__(*args, **kwargs)
        self.year = settings.get('YEAR')

    def start_requests(self):
        util = UtilClass(self.year)
        authors = util.getAuthor()
        for author in authors:
            a = author.split('-')
            code = a[1]
            url = 'https://kns.cnki.net/kcms/detail/knetsearch.aspx?sfield=au&skey=' + a[0] + '&code=' + code
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                cb_kwargs={
                    'code': code,
                    'url': url
                },
            )

    def parse(self,response,code,url):
        item = AuthorItem()
        item['code'] = code
        item['name'] = response.xpath('//h1/text()').extract_first()
        h3 = response.xpath('//h3')
        if(len(h3) >= 2):
            item['school'] = h3[0].xpath('./span/a/text()').extract_first()
            item['category'] = h3[1].xpath('./span/text()').extract_first()
        h5 = response.xpath('//h5/em/text()').extract()
        if(len(h5) > 2):
            item['upload_amount'] = h5[0]
            item['download_amount'] = h5[1]
        yield item