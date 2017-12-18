# coding:utf-8

import requests
from bs4 import BeautifulSoup

def get_content(url):
    response = requests.get(url)
    content = response.content
    return content

def totle_page(base_url):
    soup = BeautifulSoup(get_content(base_url + str(1)), 'lxml')
    totle_page = list(soup.find(class_="pagination").stripped_strings)[-2]
    return int(totle_page)

def page_url(base_url):
    for page in range(totle_page(base_url)):
        p_url = base_url + str(page)
        yield p_url

def download_image(url, filename):
    content = get_content(url)
    with open('ot_images/%s' % (filename), 'wb') as f:
        f.write(content)

def img_url(base_url):
    for page in page_url(base_url):
        html = get_content(page)
        soup = BeautifulSoup(html, 'lxml')
        img_list = soup.find_all('img', attrs={'class': 'img-responsive lazy image_dta'})
        for img in img_list:
            url = img['data-original']
            download_image(url, url[-36:])

def main():
    base_url = 'http://www.doutula.com/photo/list/?page='
    img_url(base_url)

if __name__ == '__main__':
    main()
