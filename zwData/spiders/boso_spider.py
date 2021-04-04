import os
import uuid

import scrapy
from zwData.items import BosoItem
from zwData.spiders.util import UtilClass


class BosoSpider(scrapy.Spider):
    name = "boso"
    allowned_domains = ["kns.cnki.net"]

    # 获取setting中的年份和是否在解析失败的链接内容
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = cls(crawler.settings, *args, **kwargs)
        spider._set_crawler(crawler)
        return spider

    def __init__(self, settings, *args, **kwargs):
        super(BosoSpider, self).__init__(*args, **kwargs)
        self.year = settings.get('YEAR')
        self.getError = settings.get('getError')

    def start_requests(self):
        base_url = 'https://kns.cnki.net/KCMS/detail/detail.aspx?'
        util = UtilClass(self.year)
        if (self.getError):
            links = util.getErrorUrl('boso')
        else:
            links = util.getLinks('boso')
        for link in links:
            url = base_url + link
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                cb_kwargs={
                    'url': url
                }
            )

    def parse(self,response,url):
        item = BosoItem()
        item['type'] = 'boso'
        item['year'] = self.year
        item['url'] = url
        # 根据link链接生成唯一uid，散列是SHA1，去除-
        uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, url))
        suid = ''.join(uid.split('-'))
        item['uid'] = suid
        item['title'] = response.xpath('//div[@class="wx-tit"]/h1/text()').extract_first()
        summary = response.xpath('//span[@id="ChDivSummary"]/text()').extract_first()
        if summary:
            item['summary'] = summary.replace('\n', '').replace('\r', ' ')
        keywordsfuncs = response.xpath('//div[@class="brief"]/div/p[@class="keywords"]/a/@onclick').extract()
        keywords = ""
        for k in keywordsfuncs:
            k = k.strip().split("'")
            keywords = keywords + ";" + k[3] + "-" + k[7]
        item['keywords'] = keywords[1:]
        brief = response.xpath('//div[@class="wx-tit"]/h3/span')
        if(len(brief)>=2):
            authors = brief[0]
            if authors.xpath('./a'):
                authorfuncs = authors.xpath('./a/@onclick').extract()
                authors = ""
                for a in authorfuncs:
                    a = a.strip().split("'")
                    author = a[3] + '-' + a[5]
                    authors = authors + "&" + author
                item['authors'] = authors[1:]
            else:
                item['authors'] = authors.xpath('./text()').extract_first() + "-null"
            school = brief[1]
            if school.xpath('./a'):
                item['organs'] = school.xpath('./a/text()').extract_first().strip()
            else:
                item['organs'] = school.xpath('./text()').extract_first()
        top_space = response.xpath('//li[@class="top-space"]')
        for space in top_space:  # 存在不同文献格式不同，只能判断标题名称
            title = space.xpath('./span/text()').extract_first()
            content = space.xpath('./p/text()').extract_first()
            if title == 'DOI：':
                item['DOI'] = content
            if title == '来源数据库：':
                item['db'] = content
            if title == '专辑：':
                item['special'] = content
            if title == '专题：':
                item['subject'] = content
            if title == '分类号：':
                item['cate_code'] = content
        rows = response.xpath('//div[@class="row"]')
        for row in rows:
            title = row.xpath('./span/text()').extract_first()
            if title == '导师：':
                if row.xpath('./p/a'):
                    mentorfuncs = row.xpath('./p/a/@onclick').extract_first()
                    m = mentorfuncs.strip().split("'")
                    item['mentor'] = m[3] + '-' + m[5]
                else:
                    item['mentor'] = row.xpath('./p/text()').extract_first()
        yield item