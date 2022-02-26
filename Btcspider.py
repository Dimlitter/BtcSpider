from lxml import etree
import requests

class BtcSpider():
    def __init__(self):
        self.url = 'https://mytokencap.com/currency/btc/49653'

    def get_html(self,url):
        headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        "accept-encoding": "gzip, deflate, br",
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'max-age=0',
        'cookie':'Hm_lvt_42ea409f1dfb55e7603f23c9e1b7ebbf=1645856422; Hm_lpvt_42ea409f1dfb55e7603f23c9e1b7ebbf=1645856427',
        'dnt': '1',
        'referer': 'https://mytokencap.com/',
        'if-none-match': '"d714c-X5VFwdSn8uWR68A+wqc1z4xoBwQ"',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
    }
        html = requests.get(url, headers=headers)
        return html.text

    def parse_html(self,html):
        html = etree.HTML(html)
        btc_price = html.xpath('//*[@id="__layout"]/div/div[1]/section/div[1]/div[2]/div/div[1]/div[2]/div[1]/div[1]/text()')
        for price in btc_price:
            btc = price.strip()
        print("the price of bitcion now is: ", btc)

        lowest_price = html.xpath('//*[@id="__layout"]/div/div[1]/section/div[1]/div[2]/div/div[1]/div[2]/div[3]/div[1]/div[1]/span[1]/text()')
        for price in lowest_price:
            lowest_price = price.strip()
        print("the lowest price of bitcion now is: ", lowest_price)

        highest_price = html.xpath('//*[@id="__layout"]/div/div[1]/section/div[1]/div[2]/div/div[1]/div[2]/div[3]/div[1]/div[3]/span[1]/text()')
        for price in highest_price:
            highest_price = price.strip()
        print("the highest price of bitcion now is: ", highest_price)

        return btc,lowest_price,highest_price

    def edgealarm(btc,lowest_price,highest_price):

        if float(lowest_price) < float(btc):
            print("the price of bitcion is rising")
        elif float(highest_price) > float(btc):
            print("the price of bitcion is falling")
        else:
            print("the price of bitcion is stable")
        
    def run(self):
        try:
            html = self.get_html(self.url)
            result = self.parse_html(html)
            self.edgealarm(result)
        except Exception as e:
            print(e)
        finally:
            print("the program is over")

BtcSpider().run()