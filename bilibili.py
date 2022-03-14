
from lxml import etree
from DecryptLogin import login
import requests

class bilibililogin:

    def login(self):
        lg = login.Login()
        infos_return, session = lg.bilibili('', '', 'scanqr')
        print(infos_return)
        return session

    def FetchUserInfo(self,session):
        requests.session = session
        url = 'https://www.bilibili.com/'
        requests.get(url)
        if requests.status_code == 200:
            print('获取网页成功')
        else:
            print('获取网页失败')

        html = requests.text
        html = etree.HTML(html)
        user_name = html.xpath('//*[@id="i_cecream"]/div[1]/div[1]/ul[2]/li[1]/div[2]/div/div/a[2]/text()')
        print("当前用户名：",user_name)

        user_level = html.xpath('//*[@id="i_cecream"]/div[1]/div[1]/ul[2]/li[1]/div[2]/div/div/div[2]/div/text()')
        print(user_name,user_level)

        user_coin = html.xpath('//*[@id="i_cecream"]/div[1]/div[1]/ul[2]/li[1]/div[2]/div/div/div[1]/a[1]/span[2]/text()')
        print(user_name,"硬币：",user_coin)

    def run(self):
        session = self.login()
        self.FetchUserInfo(session)


if __name__ == '__main__':
    bilibililogin = bilibililogin()
    bilibililogin.run()
        


