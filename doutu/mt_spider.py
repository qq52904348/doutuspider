# coding:utf-8

import requests
from bs4 import BeautifulSoup
import threading

#定义全局变量及锁
page_list=[]
face_list=[]
gLock=threading.Lock()

#获取网站内容
def get_content(url):
    response = requests.get(url)
    content = response.content
    return content

#获取总斗图啦总页数
def totle_page(base_url):
    soup = BeautifulSoup(get_content(base_url + str(1)), 'lxml')
    totle_page = list(soup.find(class_="pagination").stripped_strings)[-2]
    return int(totle_page)

# def page_url(base_url):
#     for page in range(totle_page(base_url)):
#         page_list.append(base_url+str(page))
#     return page_list

        # p_url = base_url + str(page)
        # yield p_url

def download_image(url,filename):
    content = get_content(url)
    with open('mt_images/%s' % (filename), 'wb') as f:
        f.write(content)

# def img_url(base_url):
#     try:
#         f=page_url(base_url)
#         while True:
#             page=next(f)
#             html = get_content(page)
#             soup = BeautifulSoup(html, 'lxml')
#             img_list = soup.find_all('img', attrs={'class': 'img-responsive lazy image_dta'})
#             for img in img_list:
#                 url = img['data-original']
#                 download_image(url,url[-36:])
#     except StopIteration:
#         pass

#运用生产者-消费者模型，face_list相当于售货机，采用多线程：
#生产者把表情链接传给face_list
def producer():
    while True:
        gLock.acquire()
        if len(page_list)==0:
            gLock.release()
            break
        else:
            page_url=page_list.pop()
            gLock.release()
            html = get_content(page_url)
            soup = BeautifulSoup(html, 'lxml')
            img_list = soup.find_all('img', attrs={'class': 'img-responsive lazy image_dta'})
            gLock.acquire()
            for img in img_list:
                url = img['data-original']
                face_list.append(url)
            gLock.release()

#消费者从face_list中取出表情链接并下载
def customer():
    while True:
        gLock.acquire()
        if len(face_list)==0:
            gLock.release()
            continue
        else:
            face_url=face_list.pop()
            gLock.release()
            download_image(face_url, face_url[-36:])

def main():
    base_url = 'http://www.doutula.com/photo/list/?page='
    for page in range(totle_page(base_url)):
        page_list.append(base_url + str(page))

#生产者3线程
    for i in range(3):
        th=threading.Thread(target=producer)
        th.start()

#消费者5线程
    for i in range(5):
        th=threading.Thread(target=customer)
        th.start()

if __name__ == '__main__':
    main()
