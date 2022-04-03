import requests
import time
import datetime
from lxml import etree
import csv
import re
from multiprocessing.dummy import Pool as ThreadPool

class novelContentSpider():
    def __init__(self):
        daynow = datetime.datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT') 
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'max-age=0',
            'dnt': '1',
            'if-modified-since': daynow,
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
        }
    def getIndex(self,url):
        time.sleep(1)
        formerindex = requests.get(url,headers=self.headers)
        formerindex.encoding = 'gb2312'
        index = etree.HTML(formerindex.text)
        chapter = index.xpath('//ul[@class="clearfix"]/li')
        chapter = len(chapter)
        return chapter

    def geturls(self,url,chapter):
        originalurl = re.findall('(https://www.trxs.cc/tongren/.*?).html',url)[0]
        urls = []
        for num in range(1,int(chapter)+1):
            url = originalurl + f'/{num}.html'
            urls.append(url)
        return urls

    def getcontent(self,url):
        flag = False
        res = ''
        chapter = re.findall('https://www.trxs.cc/tongren/.*?/(.*?)\.html',url)[0]
        while not flag:
            try:
                time.sleep(1)
                print('开始正在爬取',chapter,'章',end='\n')
                contents = requests.get(url,headers=self.headers,timeout=3)
                contents.encoding = 'gb2312'
                c = etree.HTML(contents.text)
                contents = c.xpath('//div[@class="read_chapterDetail"]/p/text()')
                result = "\n".join(contents)
                res =  res + "\n"+ result
                flag = True
            except: 
                time.sleep(10)
                flag = False
                     
        return res
    def read_csv(self):
        novel = {}
        with open("./novels.csv", 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                novel_name = row['novel_name']
                novel_size = row['novel_size']
                updatetime = row['updatetime']
                novel_url = row['novel_url']
                novel_info = row['novel_info']

                novel[novel_name] = {
                    'novel_name':novel_name,
                    'novel_size': novel_size,
                    'updatetime': updatetime,
                    'novel_url': novel_url,
                    'novel_info': novel_info,
                }
                novel_name_all = novel.keys()
        #print(novel_name_all)
        return novel,novel_name_all

    def geturl(self,novel,novel_name_all):
        for novel_name in novel_name_all:
            print("正在爬取《"+novel_name+"》")
            url = novel[novel_name]['novel_url']
            chapter = self.getIndex(url)
            urls = self.geturls(url,chapter)

            pool = ThreadPool(processes=20)
            res = pool.map(self.getcontent,urls)
            pool.close()
            pool.join()
            self.write(res,novel_name)
    def write(self,res,novel_name):
        res = "".join(res)
        #novel_name = re.findall("[\u4e00-\u9fa5a-zA-Z0-9():,\?!-？！]+",novel_name)
        #novel_name = "".join(novel_name)
        with open(f'./novels/{novel_name}.txt','w',encoding='utf-8') as f:
            f.write(res)
    def run(self):
        novel,novel_name_all = self.read_csv()
        self.geturl(novel,novel_name_all)

if __name__ == '__main__':
    Novel = novelContentSpider()
    Novel.run()