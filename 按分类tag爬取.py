# 禁满天堂地址发 https://jmcomic2.bet/
# 内地网站  jm-comic3.art
# 2023/7/24

import hashlib
import os
import re
import time
from Crypto.Hash import MD5
from PIL import Image
import requests
from lxml import etree
from tqdm import tqdm
# def convertImg(img_url):

rule=[2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
def convertImg(img_url,piece):
    img = Image.open(img_url)
    img_size = img.size
    img_crop_size = int(img_size[1] / piece)
    img_crop_size_last = (img_size[1] / piece) - img_crop_size  # 解决图片height不能被piece整除导致拼接后下方黑条
    img_crop_size_last = round(img_crop_size_last, 1)
    if img_crop_size_last > 0:  # 只有无法整除时才将新建图片进行画布纵向减小
        img_crop_size_last_sum = int(img_crop_size_last * piece)
    else:
        img_crop_size_last_sum = 0
    img_width = int(img_size[0])
    img_block_list = [] #定义一个列表用来存切割后图片
    for img_count in range(piece):
        img_crop_box = (0, img_crop_size*img_count, img_width, img_crop_size*(img_count+1))
        img_crop_area = img.crop(img_crop_box)
        img_block_list.append(img_crop_area)
    img_new = Image.new('RGB', (img_size[0], img_size[1]-img_crop_size_last_sum))
    count = 0
    for img_block in reversed(img_block_list):
        img_new.paste(img_block, (0, count*img_crop_size))
        count += 1
    #img_new.show() # 调试显示转化后的图片
    img_new.save(img_url)
def main(chapterId):
    url=f"https://jm-comic3.art/photo/{chapterId}"
    # print(url)
    headers={"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
             "referer":"https://jm-comic3.art/",
             "Upgrade-Insecure-Requests":"1",
             "Cache-Control":"max-age=0",
             "Cookie":'__atuvc=2%7C10; __cf_bm=h5vENpM3BRM5OgsSXamg8WL.ESQ.fbDCLlWe1XagIu4-1690177081-0-AQbZoCcbqcyHlOSiSGfj/6W3XBdlB4UowB1f1XTQoO2S8KGEtfhUncGHQXJKdeWmp61MGE1YP0QYxXnpRn8Qh9Y=; cf_chl_2=32ac54dc3ab8a5d; cf_chl_rc_i=1; ipcountry=HK; AVS=sefnm413j33k3no290861btuik; __cflb=0H28upDU8NsKZgZasBLVecmJrhPLJK7zt843JrUiJRz; login_reminder=1; cf_clearance=hOyjBlQDIS_9EdHT.O2qtYtqOONgmqPobKDme8XvqH8-1690177102-0-0.2.1690177102; cover=1; shuntflag=1; _gid=GA1.2.1132632628.1690177391; _ga_C1BGNGMN6J=GS1.2.1690177481.1.0.1690177481.0.0.0; ipm5=28478eea17f099e7389a72651b2dd22c; _ga_VW05C6PGN3=GS1.1.1690177395.3.1.1690177496.58.0.0; _ga=GA1.2.367152056.1678171000',
             }
    resp=requests.get(url,headers=headers)
    # print(resp.text)
    if resp.status_code==200:
        html=etree.HTML(resp.text)
        img_urls=html.xpath('//*[@class="center scramble-page"]/img/@data-original')
        for img_url in img_urls:

            print(img_url)
            img_name=img_url.split('?v=')[0].split('/')[-1]
            # print(img_name)
            # filename="P1/"
            filename=etree.HTML(resp.text).xpath('/html/head/title/text()')[0]
            filename = re.sub('[\/:*?"<>|]', '-', filename)+'/'
            filename=title+filename
            if not os.path.exists(filename):
                os.mkdir(filename)

            # # if not os.path.exists(filename+img_name):
            # try:
            #     res=requests.get(img_url)
            # except:
            #     time.sleep(5)
            #     print("图片下载失败")
            #     res = requests.get(img_url)
            # with open(filename+img_name,mode="wb")as f:
            #     f.write(res.content)
            # print(img_name+"下载完成")

            # if not os.path.exists(filename+img_name):
            try:
                res=requests.get(img_url)
            except:
                time.sleep(5)
                print("图片下载失败")
                res = requests.get(img_url)
            with open(filename+img_name,mode="wb")as f:
                f.write(res.content)
            print(img_name+"下载完成")

            # img = Image.open(filename+img_name)
            # img_size = img.size
            # print(img_size)
            # 图片处理
            # 获取图片切割的片数
            # 禁漫天堂最新的切割算法, 不再固定切割成10份, 而是需要通过chapterId和photoId共同确定分割块数.
            if chapterId>268850:
                piece=10
                photoId=img_name.split('.')[0]
                biaoshi=f"{chapterId}{photoId}"
                # print(biaoshi)
                hl = hashlib.md5()
                # 更新hash对象的值，如果不使用update方法也可以直接md5构造函数内填写
                # md5_obj=hashlib.md5("123456".encode("utf-8")) 效果一样
                hl.update(biaoshi.encode("utf-8"))
                c=hl.hexdigest()
                # print(c)
                mod=10
                if chapterId>=421926:
                    mod=8
                piece=rule[ord(c[-1])%mod]
                # print(piece)
                # reverseImage(filename+img_name,chapterId,piece)
                convertImg(filename+img_name,piece)

            # break
if __name__ == '__main__':

    page=0
    while page<20:
        page=page+1
        url=f"https://jm-comic3.art/search/photos?search_query=%E5%8E%9F%E7%A5%9E&main_tag=1&o=mv&page={page}"
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "referer": "https://jm-comic3.art/",
            "Upgrade-Insecure-Requests": "1",
            "Cache-Control": "max-age=0",
            "Cookie": '__atuvc=2%7C10; __cf_bm=h5vENpM3BRM5OgsSXamg8WL.ESQ.fbDCLlWe1XagIu4-1690177081-0-AQbZoCcbqcyHlOSiSGfj/6W3XBdlB4UowB1f1XTQoO2S8KGEtfhUncGHQXJKdeWmp61MGE1YP0QYxXnpRn8Qh9Y=; cf_chl_2=32ac54dc3ab8a5d; cf_chl_rc_i=1; ipcountry=HK; AVS=sefnm413j33k3no290861btuik; __cflb=0H28upDU8NsKZgZasBLVecmJrhPLJK7zt843JrUiJRz; login_reminder=1; cf_clearance=hOyjBlQDIS_9EdHT.O2qtYtqOONgmqPobKDme8XvqH8-1690177102-0-0.2.1690177102; cover=1; shuntflag=1; _gid=GA1.2.1132632628.1690177391; _ga_C1BGNGMN6J=GS1.2.1690177481.1.0.1690177481.0.0.0; ipm5=28478eea17f099e7389a72651b2dd22c; _ga_VW05C6PGN3=GS1.1.1690177395.3.1.1690177496.58.0.0; _ga=GA1.2.367152056.1678171000',
            }
        res=requests.get(url,headers=headers)
        # print(res.text)
        head="https://jm-comic3.art"
        list=[]
        hrefs=etree.HTML(res.text).xpath('//*[@id="wrapper"]/div[@class="container"]/div[@class="row"]/div/div[@class="row m-0"]/div/div[@style]/a/@href')
        for href in hrefs:
            # print(href)
            href=head+href
            list.append(href)
        hrefs=etree.HTML(res.text).xpath('//*[@id="wrapper"]/div[@class="container"]/div[@class="row"]/div/div[@class="row"]/div/div[@style]/a/@href')
        for href in hrefs:
            # print(href)
            href=head+href
            list.append(href)
        # print(list)
        # for list in list:
        i=2
        if i<len(list):
            list=list[i]
            resp=requests.get(list)
            href_vs=etree.HTML(resp.text).xpath('//*[@id="episode-block"]//ul/a/@data-album')
            title=etree.HTML(resp.text).xpath('/html/head/meta[@property="og:title"]/@content')[0]
            title = re.sub('[\/:*?"<>|]', '-', title)+'/'
            print(title)
            if not os.path.exists(title):
                os.mkdir(title)
            if len(href_vs)!=0:
                for href_v in href_vs:
                    chapterId=int(href_v)
                    # print(chapterId)
                    main(chapterId)
            else:
                # print(list.replace('/'+list.split('/')[-1],'').split('/')[-1])
                chapterId=int(list.replace('/'+list.split('/')[-1],'').split('/')[-1])
                # print(chapterId)
                main(chapterId)

        break

