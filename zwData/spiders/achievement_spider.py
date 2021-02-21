import os
import uuid

import scrapy

from zwData.items import AchievementItem
from zwData.spiders.util import UtilClass


class AchievementSpiderSpider(scrapy.Spider):
    name = 'achievement'
    allowed_domains = ['kns.cnki.net']

    def start_requests(self):
        self.year = '2020'
        base_url = 'https://kns.cnki.net/kcms/detail/detail.aspx?'
        base_path = 'target/' + self.year + '/'
        util = UtilClass(self.year)
        links = util.getLinks(base_path, 'achievement')
        for link in links:
        # link = 'dbcode=SNAD&dbname=SNAD&filename=SNAD000001855707'
            url = base_url + link
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                cb_kwargs={
                    'url': url
                },
            )
        print("爬取完成")

    def parse(self, response, url):
        item = AchievementItem()
        item['type'] = 'achievement'
        item['year'] = self.year
        item['url'] = url
        # 根据link链接生成唯一uid，散列是SHA1，去除-
        uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, url))
        suid = ''.join(uid.split('-'))
        item['uid'] = suid
        item['title'] = response.xpath('//h1/text()').extract_first()
        rows = response.xpath('//div[@class="row"]')
        for row in rows:
            title = row.xpath('./span/text()').extract_first()
            content = row.xpath('./p/text()').extract_first()
            if title == '成果完成人：':
                item['authors'] = content
            if title == '第一完成单位：':
                item['organ'] = content
            if title == '关键词：':
                item['keywords'] = content
            if title == '中图分类号：':
                item['book_code'] = content
            if title == '学科分类号：':
                item['subject_code'] = content
            if title == '成果简介：':
                item['summary'] = content
            if title == '成果类别：':
                item['category'] = content
            if title == '成果入库时间：':
                item['in_time'] = content
            if title == '成果水平：':
                item['level'] = content
            if title == '研究起止时间：':
                item['pass_time'] = content
            if title == '评价形式：':
                item['evaluate'] = content
        yield item