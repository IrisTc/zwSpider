# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class ZwdataPipeline:
    def __init__(self, settings):
        self.year = settings.get('YEAR')

    # 拿到setting中的年份
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_item(self, item, spider):
        if spider.name == 'link' or spider.name == 'link-error':
            if item['db'] == '期刊':
                with open('target/' + self.year + '/journal_' + item['code'] + '.txt', 'a', encoding='utf-8') as f:
                    f.write(item['url'] + '\n')
            if item['db'] == '博士' or item['db'] == '硕士':
                with open('target/' + self.year + '/boso_' + item['code'] + '.txt', 'a', encoding='utf-8') as f:
                    f.write(item['url'] + '\n')
            if item['db'] == '科技成果':
                with open('target/' + self.year + '/achievement_' + item['code'] + '.txt', 'a', encoding='utf-8') as f:
                    f.write(item['url'] + '\n')
            return item
        if spider.name == 'journal' or spider.name == 'boso' or spider.name == 'achievement':
            return item
