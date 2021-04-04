import os
import time

import arrow
import requests


class UtilClass():
    def __init__(self, year):
        self.year = year
        self.codeFile = 'target/' + year + '/code.txt'

    # 所有分类代码
    def getCodeAll(self):
        with open(self.codeFile, 'r') as f:
            all = f.read()
            return all.split()

    # 拿到没爬过的分类代码
    def getCode(self):
        codes = self.getCodeAll()
        for i in range(len(codes)):
            code = codes[i]
            if '_' in code:
                continue
            else:
                self.markCode(i)
                return code

    # 标记已经爬过的分类代码
    def markCode(self, num):
        with open(self.codeFile, 'r') as f:
            all = f.read()
            lines = all.split()
            lines[num] = '_' + lines[num]
            new = ('\n').join(lines)
        with open(self.codeFile, 'w+') as f:
            f.write(new)

    # 获取一年内的天数
    def getAllDayPerYear(self):
        start_date = '%s-1-1' % self.year
        a = 0
        all_date_list = []
        days_sum = isLeapYear(int(self.year))
        while a < days_sum:
            b = arrow.get(start_date).shift(days=a).format("YYYY-MM-DD")
            a += 1
            all_date_list.append(b)
        return all_date_list

    # 获取文件类的链接
    def getLinks(self,type):
        base_path = 'target/' + self.year + '/'
        files = os.listdir(base_path)
        for file in files:
            if '-' in file:
                continue
            file_path = base_path + file
            if type in file:
                print('开始爬取文件' + file)
                with open(file_path, 'r') as fp:
                    all = fp.read()
                links = all.split('\n')
                os.rename(file_path, base_path + '-' + file)
                break
        return links

    def getErrorUrl(self, type):
        file_path = 'error/'
        file_name = type + 'error.txt'
        with open(file_path + file_name, 'r') as fp:
            all = fp.read()
        links = all.split('\n')
        os.rename(file_path + file_name, file_path + '-' + file_name)
        return links

    # 获取errorday
    def getDay(self):
        base_path = 'error/'
        files = os.listdir(base_path)
        for file in files:
            if '-' in file:
                continue
            if 'errorday' in file:
                file_path = base_path + file
                print('开始爬取文件' + file)
                with open(file_path, 'r') as fp:
                    all = fp.read()
                days = all.split('\n')
                os.rename(file_path, base_path + '-' + file)
                break
        return days

    # 获取errrorpage
    def getPage(self):
        base_path = 'error/'
        files = os.listdir(base_path)
        for file in files:
            if '-' in file:
                continue
            if 'errorpage' in file:
                file_path = base_path + file
                print('开始爬取文件' + file)
                with open(file_path, 'r') as fp:
                    all = fp.read()
                pages = all.split('\n')
                os.rename(file_path, base_path + '-' + file)
                break
        return pages

    # 循环获取erpage
    def getErPage(self):
        file_path = 'error/erpage.txt'
        size = os.path.getsize(file_path)
        print(size)
        if size == 0:
            return []
        else:
            with open(file_path, 'r') as fp:
                all = fp.read()
            pages = all.split('\n')
            os.remove(file_path)
            return pages

    def getAuthor(self):
        base_path = './author_output/'
        files = os.listdir(base_path)
        for file in files:
            if '-' in file:
                continue
            else:
                file_path = base_path + file
                with open(file_path, 'r', encoding='utf-8') as fp:
                    all = fp.read()
                authors = all.split('\n')
                os.rename(file_path, base_path + '-' + file)
                break
        return authors

    def markSecondError(self,code,date,pagenum):
        if pagenum == 0:
            with open('error/erday.txt', 'a', encoding='utf-8') as f:
                f.write(code + '&' + date + '\n')
        else:
            with open('error/erpage.txt', 'a', encoding='utf-8') as f:
                f.write(code + '&' + date + '&' + str(pagenum) + '\n')


    # 获取cookies
    def getCookies(self,date,code):
        search_url = 'https://kns.cnki.net/kns/request/SearchHandler.ashx/'
        now_time = time.strftime('%a %b %d %Y %H:%M:%S') + ' GMT+0800 (中国标准时间)'
        params = {
            "action": "",
            "NaviCode": code,
            "ua": "1.21",
            "isinEn": "1",
            "PageName": "ASP.brief_result_aspx",
            "DbPrefix": "SCDB",
            "DbCatalog": "中国学术文献网络出版总库",
            "ConfigFile": "SCDB.xml",
            "db_opt": "CJFQ,CJRF,CJFN,CDFD,CMFD,CPFD,IPFD,CCND,BDZK,CISD,SNAD,CCJD",
            "publishdate_from": date,
            "publishdate_to": date,
            "CKB_extension": "ZYW",
            "his": "0",
            '__': now_time
        }
        session_response = requests.get(search_url, params=params)
        cookies = requests.utils.dict_from_cookiejar(session_response.cookies)
        return cookies

def isLeapYear(years):
    assert isinstance(years, int), "请输入整数年，如 2018"
    if ((years % 4 == 0 and years % 100 != 0) or (years % 400 == 0)):  # 判断是否是闰年
        return 366
    else:
        return 365