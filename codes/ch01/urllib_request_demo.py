#!/usr/bin/env python
# encoding: utf-8
"""
@file: urllib_request_demo.py
@time: 2022/1/13 18:44
@project: web-crawler
@desc: 
"""
import urllib.request

url = 'https://www.python.org'
response = urllib.request.urlopen(url)
# 打印网页源代码
print(response.read().decode('utf-8'))
