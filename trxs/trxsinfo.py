import requests
from lxml import etree
import time
import datetime
import csv
import re

class novelSpider():
    def __init__(self,page):
        self.url = 'https://www.trxs.cc/tongren/'
        self.page = page
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

    def get_html(self,url):
        r = requests.get(url, headers=self.headers)
        r.encoding = 'gb2312'
        if r.status_code == 200:
            print('获取网页成功')
        else:
            print('获取网页失败')
        return r.text , url

    def parse_html(self, html,url):
        html = etree.HTML(html)
        if url == self.url:
            page = 1
        else:
            page = re.search('https://www.trxs.cc/tongren/index_(\d+?)\.html', url).group(1)
        novels = {}
        for i in range(1, 11):
            index = '第'+f'{page}'+'页'+f'{i}'+'篇'

            novel_names = html.xpath(f'/html/body/div[4]/div/div[1]/div[{i}]/a/div[2]/h3/text()')

            novel_size = html.xpath(f'/html/body/div[4]/div/div[1]/div[{i}]/a/div[2]/div/label[1]/text()')
                                    
            updatetime = html.xpath(f'/html/body/div[4]/div/div[1]/div[{i}]/a/div[2]/div/label[2]/text()')

            novel_url = html.xpath(f'/html/body/div[4]/div/div[1]/div[{i}]/a/@href')

            novel_infos = html.xpath(f'/html/body/div[4]/div/div[1]/div[{i}]/a/div[2]/p/text()') 
            
            for novel_name, novel_size, updatetime, novel_url ,novel_infos in zip(novel_names, novel_size, updatetime, novel_url,novel_infos):
                novels[index] = [{
                    'novel_name': novel_name,
                    'novel_size': novel_size,
                    'updatetime': updatetime,
                    'novel_url': "https://www.trxs.cc" + novel_url,
                    'novel_info': novel_infos
                }]
        #print(novels)
        return novels,page
        
    def save_novel(self, novels,page):
        if len(novels) == 0:
            print('没有小说')
        else:
            with open('./novels.csv', 'w',newline = '',encoding = 'utf-8') as f:
                header = ['novel_name', 'novel_size', 'updatetime', 'novel_url','novel_info']
                writer = csv.DictWriter(f,header, delimiter = ',')
                writer.writeheader()
                for page_index in range(1,int(page)+1):
                    for i in range(1, int(len(novels)/int(page))):
                        writer.writerows(novels['第'+f'{page_index}'+'页'+f'{i}'+'篇'])
                print('保存成功')

                

    def run(self):
        novels_all = {}
        for i in range(1,self.page):
            if i == 1:
                url = self.url
            else:
                url = self.url + 'index_'+ str(i) + '.html'
            html,url = self.get_html(url)
            time.sleep(5)
            novels,page= self.parse_html(html,url)
            novels_all.update(novels)
            print(novels_all)
        print("最终的结果是",novels_all)
        self.save_novel(novels_all,page)

if __name__ == '__main__':
    novel = novelSpider(5)
    novel.run()