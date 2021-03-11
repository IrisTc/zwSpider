# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class ZwdataSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ZwdataDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        if response.status != 200:
            key = request.cb_kwargs
            if spider.name == 'link':
                if 'pagenum' in key:
                    pagenum = key['pagenum']
                else:
                    pagenum = 0
                self.markFirstError(key['code'], key['date'], pagenum)
                return response
            elif 'error' in spider.name:
                if 'pagenum' in key:
                    pagenum = key['pagenum']
                else:
                    pagenum = 0
                self.markSecondError(key['code'], key['date'], pagenum)
            else:
                self.markLinkError(key['url'], spider.name)
        else:
            return response

    def process_exception(self, request, exception, spider):
        key = request.cb_kwargs
        if spider.name == 'link':
            if 'pagenum' in key:
                pagenum = key['pagenum']
            else:
                pagenum = 0
            self.markFirstError(key['code'],key['date'],pagenum)
        elif 'error' in spider.name:
            if 'pagenum' in key:
                pagenum = key['pagenum']
            else:
                pagenum = 0
            self.markSecondError(key['code'],key['date'],pagenum)
        else:
            self.markLinkError(key['url'],spider.name)
        return None

    def markLinkError(self,url,type):
        if type == 'journal':
            with open('error/journalerror.txt', 'a', encoding='utf-8') as file:
                file.write(url + '\n')
        if type == 'boso':
            with open('error/bosoerror.txt', 'a', encoding='utf-8') as file:
                file.write(url + '\n')
        if type == 'achievement':
            with open('error/achivementerror.txt', 'a', encoding='utf-8') as file:
                file.write(url + '\n')
        if type == 'author':
            with open('author/error.txt','a', encoding='utf-8') as file:
                file.write(url + '\n')

    def markSecondError(self,code,date,pagenum):
        if pagenum == 0:
            with open('error/erday.txt', 'a', encoding='utf-8') as f:
                f.write(code + '&' + date + '\n')
        else:
            with open('error/erpage.txt', 'a', encoding='utf-8') as f:
                f.write(code + '&' + date + '&' + str(pagenum) + '\n')

    def markFirstError(self, code, date, pagenum):
        if pagenum == 0:
            with open('error/errorday_' + date + '.txt', 'a', encoding='utf-8') as f:
                f.write(code + '&' + date + '\n')
        else:
            with open('error/errorpage_' + date + 'txt', 'a', encoding='utf-8') as f:
                f.write(code + '&' + date + '&' + str(pagenum) + '\n')

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
