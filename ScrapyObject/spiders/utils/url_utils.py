# -*- coding: utf-8 -*-
import re
from posixpath import normpath
from urllib import parse
from urllib.parse import urljoin, urlparse, urlunparse

import chardet
import scrapy
from bs4 import BeautifulSoup

from ScrapyObject.items import VideoBean


def format_url_one(video_url):
    """ 格式化url
    """
    return video_url.replace("\\/", "/")


def format_url_two(video_url):
    """ 格式化url
    """
    return parse.unquote(video_url)


def get_video_item(id, name='', tags='', purl='', vurl=''):
    """ 获取视频数据
    """
    item = VideoBean()
    item['id'] = id
    item['name'] = name
    item['tags'] = tags
    item['pUrl'] = purl
    item['vUrl'] = vurl
    return item


def get_video_url_one(content):
    """ 获取视频地址
    """
    return re.findall(
        r'http.*?\.M3U8|http.*?\.MP4|http.*?\.WMV|http.*?\.MOV|http.*?\.AVI|http.*?\.MKV|http.*?\.FLV|http.*?\.RMVB|http.*?\.3GP',
        content, re.IGNORECASE)


# 得到返回结果
def get_data(response):
    return response.body.decode(chardet.detect(response.body)['encoding'], 'ignore')


# 从传入的字符串中取出所有url并返回
def get_url(content):
    # return  re.findall('"((http|ftp)s?://.*?)"', content)
    # return re.findall(r'href\=\"(http\:\/\/[a-zA-Z0-9\.\/]+)\"', content)
    return re.findall(r"(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')", content)


# 把url添加进请求队列
def add_request(response, callback, str_data=None):
    if str_data == None:
        str_data = get_data(response)
    for k in get_url(str_data):
        if k.startswith('/'):
            split_joint('http://www.yjizz5.com', k)
        else:
            full_url = response.urljoin(k)
        yield scrapy.Request(full_url, callback=callback)


# 把数据保存到文件中
def save_data(data, file_name):
    file = open(file_name, 'a+')
    file.write(data + '\r\n')
    file.close()


# url拼接
def split_joint(base, url):
    url1 = urljoin(base, url)
    arr = urlparse(url1)
    path = normpath(arr[2])
    return urlunparse((arr.scheme, arr.netloc, path, arr.params, arr.query, arr.fragment))


# url拼接
def get_url_two(content, base):
    s = set()
    soup = BeautifulSoup(content, 'html.parser')  # 文档对象
    for k in soup.find_all('a'):
        if (type(k.get('href')) == str):
            if (k.get('data-attach-session') is None):
                if 'http://www.fcw45.com/playlists/' in k.get('href'):
                    # print("不添加***************       %s" % k.get('href'))
                    pass
                elif (k.get('href').startswith('/')):
                    s.add(split_joint(base, k.get('href')))
                elif (k.get('href').startswith('http') and k.get('href').endswith('mp4')):
                    pass
                    # print("视频地址***************       %s" % k.get('href'))
                elif (k.get('href').startswith('http')):
                    s.add(k.get('href'))
                elif (k.get('href').startswith('https')):
                    s.add(k.get('href'))
                else:
                    pass
                    # print("特殊的***************       %s" % k.get('href'))
    return s


# url拼接
def get_url_one(content):
    s = set()
    soup = BeautifulSoup(content, 'html.parser')  # 文档对象
    for k in soup.find_all('a'):
        if (type(k.get('href')) == str):
            if (k.get('href').startswith('/') and k.get('href').endswith('html')):
                s.add(k.get('href'))

    return s


def get_url_san(content):
    s = set()
    soup = BeautifulSoup(content, 'html.parser')  # 文档对象
    for k in soup.find_all('a'):
        if (type(k.get('href')) == str):
            if k.get('href').startswith('/video/'):
                s.add(split_joint('https://av.av699.win/', k.get('href')))

    return s
