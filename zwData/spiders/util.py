import os

import arrow

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

    # 获取文件类的连接
    def getLinks(self,base_path,type):
        files = os.listdir(base_path)
        for file in files:
            if '-' in file:
                continue
            file_path = base_path + file
            if type in file:
                print('开始爬取文件' + file)
                with open(file_path, 'r') as fp:
                    all = fp.read()
                links = all.split()
                os.rename(file_path, base_path + '-' + file)
                break
        return links

def isLeapYear(years):
    assert isinstance(years, int), "请输入整数年，如 2018"
    if ((years % 4 == 0 and years % 100 != 0) or (years % 400 == 0)):  # 判断是否是闰年
        return 366
    else:
        return 365