# -*- coding: utf-8 -*-
import requests


with requests.Session() as s:
    print(s.get(r'https://httpbin.org/get'))