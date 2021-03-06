import os
import re
import uuid
import scrapy
from zwData.items import JournalItem
from zwData.spiders.util import UtilClass


class JournalSpider(scrapy.Spider):
    name = 'journal'
    allowed_domains = ['kns.cnki.net']

    def start_requests(self):
        self.year = '2020'
        base_url = 'https://kns.cnki.net/KCMS/detail/detail.aspx?'
        base_path = 'target/'+self.year+'/'
        util = UtilClass(self.year)
        links = util.getLinks(base_path,'journal')
        for link in links:
            url = base_url + link
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                cb_kwargs={
                    'url': url
                },
            )

    def parse(self,response,url):
        item = JournalItem()
        item['type'] = 'journal'
        item['year'] = self.year
        item['url'] = url
        # 根据link链接生成唯一uid，散列是SHA1，去除-
        uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, url))
        suid = ''.join(uid.split('-'))
        item['uid'] = suid
        item['title'] = response.xpath('//h1/text()').extract_first()
        magazine = response.xpath('//div[@class="top-tip"]/span/a')
        magazinefunc = magazine.xpath('./@onclick').extract_first()
        m = magazinefunc.strip().split("'")
        item['magazine'] = magazine.xpath('./text()').extract_first() + "-pcode=" + m[1] + "&pykm=" + m[3]
        item['summary'] = response.xpath('string(//span[@id="ChDivSummary"])').extract_first()
        keywordsfuncs = response.xpath('//p[@class="keywords"]/a/@onclick').extract()
        if len(keywordsfuncs) > 0:
            keywords = ""
            for k in keywordsfuncs:
                k = k.strip().split("'")
                keywords = keywords + ";" + k[3] + "-" + k[7]
            item['keywords'] = keywords[1:]
        authorSelector = response.xpath('//h3[@class="author"]/span')
        authors = ""
        for selector in authorSelector:
            if selector.xpath('./a'):
                authorfunc = selector.xpath('./a/@onclick').extract_first()
                a = authorfunc.strip().split("'")
                author = a[3] + "-" + a[5]
            else:
                author = selector.xpath('./text()').extract_first() + "-null"
            authors = authors + "&" + author
        item['authors'] = authors[1:]
        organstr = ""
        organSelector = response.xpath('//div[@class="wx-tit"]/h3')[1]
        if organSelector.xpath('./a[@class="author"]'):
            organ_a = organSelector.xpath('./a[@class="author"]/text()').extract()
            for o in organ_a:
                organstr = organstr + o.strip()
        organ_noa = organSelector.xpath('./span/text()').extract_first()
        if organ_noa:
            organstr = organstr + organ_noa
        nonum = (re.sub(r'(\d+)', ' ', organstr)).strip()
        organlist = nonum.strip('.').split('.')
        organs = ""
        for organ in organlist:
            organs = organs + ';' + organ.strip()
        item['organs'] = organs[1:]
        top_space = response.xpath('//li[@class="top-space"]')
        for space in top_space:  # 存在不同文献格式不同，只能判断标题名称
            title = space.xpath('./span/text()').extract_first()
            content = space.xpath('./p/text()').extract_first()
            if title == 'DOI：':
                item['DOI'] = content
            if title == '分类号：':
                item['cate_code'] = content
            if title == '来源数据库：':
                item['db'] = content
            if title == '专辑：':
                item['special'] = content
            if title == '专题：':
                item['subject'] = content
        yield item