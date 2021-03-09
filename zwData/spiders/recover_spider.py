import os
import uuid

import scrapy

from zwData.items import AchievementItem
from zwData.spiders.util import UtilClass


class AchievementSpiderSpider(scrapy.Spider):
    name = 'recover'
    allowed_domains = ['kns.cnki.net']

    def start_requests(self):
        self.year = '2020'
        base_path = 'target/' + self.year + '/'
        files = os.listdir(base_path)
        type = 'boso'
        for file in files:
            if '-' in file:
                file_path = base_path + file
                if type in file:
                    os.rename(file_path, base_path + file[1:])
