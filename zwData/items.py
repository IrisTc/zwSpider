# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class LinkItem(scrapy.Item):
    url = scrapy.Field()
    db = scrapy.Field()
    code = scrapy.Field()

class JournalItem(scrapy.Item):
    type = scrapy.Field()
    year = scrapy.Field()
    url = scrapy.Field()
    uid = scrapy.Field()
    title = scrapy.Field()
    authors = scrapy.Field()
    organs = scrapy.Field()
    summary = scrapy.Field()
    keywords = scrapy.Field()
    DOI = scrapy.Field()
    special = scrapy.Field() #专辑
    subject = scrapy.Field() #专题
    cate_code = scrapy.Field() #分类号
    db = scrapy.Field() #来源数据库

    magazine = scrapy.Field() # 期刊
    mentor = scrapy.Field() # 博硕导师


class BosoItem(scrapy.Item):
    type = scrapy.Field()
    year = scrapy.Field()
    url = scrapy.Field()
    uid = scrapy.Field()
    title = scrapy.Field()
    authors = scrapy.Field()
    organs = scrapy.Field()
    summary = scrapy.Field()
    keywords = scrapy.Field()
    DOI = scrapy.Field()
    special = scrapy.Field()
    subject = scrapy.Field()
    cate_code = scrapy.Field()
    db = scrapy.Field() #来源数据库

    magazine = scrapy.Field() # 期刊
    mentor = scrapy.Field() # 博硕导师


class AchievementItem(scrapy.Item):
    type = scrapy.Field()
    year = scrapy.Field()
    url = scrapy.Field()
    uid = scrapy.Field()
    title = scrapy.Field()
    authors = scrapy.Field()
    organ = scrapy.Field() # 第一完成单位
    keywords = scrapy.Field()
    book_code = scrapy.Field() # 中图分类号
    subject_code = scrapy.Field() # 学科分类号
    summary = scrapy.Field()
    category = scrapy.Field() # 成果类别
    in_time = scrapy.Field() # 成果入库时间
    pass_time = scrapy.Field() # 研究起止时间
    level = scrapy.Field() # 成果水平
    evaluate = scrapy.Field() # 评价形式