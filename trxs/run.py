import trxsinfo
import NovelContents

def run(page):
    try:
        novel = trxsinfo.novelSpider(page)
        novel.run()
    except:
        pass

    flag = True
    while flag:
        try:
            Novel = NovelContents.novelContentSpider()
            Novel.run()
            flag = False
        except:
            flag = True

if __name__ == '__main__':
    try:
        run(50)
    except:
        print("failed")