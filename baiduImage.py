#!usr/bin/env python
# coding=utf-8

import requests
import re
import os
import urllib.parse


# 获取动态页面返回的文本
def get_page_html(page_url):
    headers = {
        'Referer': 'https://image.baidu.com/search/index?tn=baiduimage',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
    }
    try:
        r = requests.get(page_url, headers=headers)
        if r.status_code == 200:
            r.encoding = r.apparent_encoding
            return r.text
        else:
            print('请求失败')
    except Exception as e:
        print(e)


# 从文本中提取出真实图片地址
def parse_result(text):
    url_real = re.findall('"thumbURL":"(.*?)",', text)
    return url_real


# 获取图片的content
def get_image_content(url_real):
    headers = {
        'Referer': url_real,
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
    }
    try:
        r = requests.get(url_real, headers=headers)
        if r.status_code == 200:
            r.encoding = r.apparent_encoding
            return r.content
        else:
            print('请求失败')
    except Exception as e:
        print(e)


# 将图片的content写入文件
def save_pic(url_real, content):
    root = 'D://baiduimage//'
    path = root + url_real.split('/')[-1]
    if not os.path.exists(root):
        os.mkdir(root)
    if not os.path.exists(path):
        with open(path, 'wb') as f:
            f.write(content)
            print('图片{}保存成功，地址在{}'.format(url_real, path))
    else:
        pass


# 主函数
def main():
    keyword = input('请输入你要查询的关键字: ')
    keyword_quote = urllib.parse.quote(keyword)
    depth = int(input("请输入要爬取的页数(每页30张图): "))
    for i in range(depth):
        url = 'https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord+=&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&word={}&z=&ic=0&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&step_word={}&pn={}&rn=30&gsm=1e&1541136876386='.format(
            keyword_quote, keyword_quote, i * 30)
        html = get_page_html(url)
        real_urls = parse_result(html)
        for real_url in real_urls:
            content = get_image_content(real_url)
            save_pic(real_url, content)


# 函数入口
if __name__ == '__main__':
    main()
