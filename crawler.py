# -*- coding: utf-8 -*-

import pickle
import math
import os.path
import shutil
import datetime
import time
import random
import json
import re
import chardet
import string
import base64


import requests
from bs4 import BeautifulSoup


from model import TradedHouse, DistricHouse, BidHouse, RentHouse, create_table, clear_table


grabedPool = {}

gz_district = ['tianhe', 'yuexiu', 'liwan', 'haizhu', 'panyu', 'baiyun', 'huangpugz', 'conghua', 'zengcheng', 'huadou', 'luogang', 'nansha']
gz_district_name = {"tianhe":u"天河", "yuexiu":u"越秀", "liwan":u"荔湾", "haizhu":u"海珠",
        "panyu":u"番禺", "baiyun":u"白云", "huangpugz":u"黄埔", "conghua": u"从化", "zengcheng": u"增城",
        "huadou":u"花都", "luogang": u"萝岗","nansha":u"南沙"}
global start_offset
start_offset = 1

user_agent_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/531.21.8 (KHTML, like Gecko) Version/4.0.4 Safari/531.21.10",
        "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/533.17.8 (KHTML, like Gecko) Version/5.0.1 Safari/533.17.8",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.1.17) Gecko/20110123 (like Firefox/3.x) SeaMonkey/2.0.12",
        "Mozilla/5.0 (Windows NT 5.2; rv:10.0.1) Gecko/20100101 Firefox/10.0.1 SeaMonkey/2.7.1",
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; en-US) AppleWebKit/532.8 (KHTML, like Gecko) Chrome/4.0.302.2 Safari/532.8",
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.464.0 Safari/534.3",
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_5; en-US) AppleWebKit/534.13 (KHTML, like Gecko) Chrome/9.0.597.15 Safari/534.13",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.186 Safari/535.1",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.54 Safari/535.2",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7",
        "Mozilla/5.0 (Macintosh; U; Mac OS X Mach-O; en-US; rv:2.0a) Gecko/20040614 Firefox/3.0.0 ",
        "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.0.3) Gecko/2008092414 Firefox/3.0.3",
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.1) Gecko/20090624 Firefox/3.5",
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2.14) Gecko/20110218 AlexaToolbar/alxf-2.0 Firefox/3.6.14",
        "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Mozilla/5.0 (iPad; CPU OS 9_0 like Mac OS X) AppleWebKit/601.1.17 (KHTML, like Gecko) Version/8.0 Mobile/13A175 Safari/600.1.4",
        "Mozilla/5.0 (iPad; CPU OS 9_0 like Mac OS X) AppleWebKit/601.1.39 (KHTML, like Gecko) Version/9.0 Mobile/13A4305g Safari/601.1",
        "Mozilla/5.0 (iPad; CPU OS 9_0 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13A344 Safari/601.1",
        "Mozilla/5.0 (iPad; CPU OS 9_0 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) CriOS/45.0.2454.89 Mobile/13A344 Safari/600.1.4 (000205)",
        "Mozilla/5.0 (iPad; CPU OS 9_0 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) GSA/8.0.57838 Mobile/13A344 Safari/600.1.4",
        "Mozilla/5.0 (iPad; CPU OS 9_0_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13A404 Safari/601.1",
        "Mozilla/5.0 (iPad; CPU OS 9_0 like Mac OS X) AppleWebKit/631.1.17 (KHTML, like Gecko) Version/8.0 Mobile/13A171 Safari/637.1.4",
        "Mozilla/5.0 (iPad; CPU OS 9_0_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) GSA/6.0.51363 Mobile/13A404 Safari/600.1.4",
        "Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) GSA/8.0.57838 Mobile/13B5110e Safari/600.1.4",
        "Mozilla/5.0 (iPad; CPU OS 9_0_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) CriOS/45.0.2454.89 Mobile/13A404 Safari/600.1.4 (000994)",
        "Mozilla/5.0 (iPad; CPU OS 9_0_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) CriOS/45.0.2454.89 Mobile/13A404 Safari/600.1.4 (000862)",
        "Mozilla/5.0 (iPad; CPU OS 9_0_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) CriOS/45.0.2454.89 Mobile/13A404 Safari/600.1.4 (000065)",
        "Mozilla/5.0 (iPad; CPU OS 9_0_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) GSA/5.2.43972 Mobile/13A452 Safari/600.1.4",
        "Mozilla/5.0 (iPad; CPU OS 9_0_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13A452 Safari/601.1",
        "Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B5130b Safari/601.1",
        "Mozilla/5.0 (iPad; CPU OS 9_0_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) CriOS/45.0.2454.89 Mobile/13A404 Safari/600.1.4 (000539)",
        "Mozilla/5.0 (iPad; CPU OS 9_0_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) CriOS/45.0.2454.89 Mobile/13A452 Safari/600.1.4 (000549)",
        "Mozilla/5.0 (iPad; CPU OS 9_0_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) CriOS/45.0.2454.89 Mobile/13A452 Safari/600.1.4 (000570)",
        "Mozilla/5.0 (iPad; CPU OS 9_0_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) CriOS/44.0.2403.67 Mobile/13A452 Safari/600.1.4 (000693)",
        "Mozilla/5.0 (iPad; CPU OS 9_0_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) GSA/9.0.60246 Mobile/13A404 Safari/600.1.4",
        "Mozilla/5.0 (iPad; CPU OS 9_0_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) CriOS/45.0.2454.89 Mobile/13A452 Safari/600.1.4 (000292)",
        "Mozilla/5.0 (iPad; CPU OS 9_0_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) GSA/9.0.60246 Mobile/13A452 Safari/600.1.4",
        "Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B137 Safari/601.1",
        "Mozilla/5.0 (iPad; CPU OS 9_0_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) CriOS/45.0.2454.89 Mobile/13A452 Safari/600.1.4 (000996)",
        "Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1",
        "Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) CriOS/46.0.2490.73 Mobile/13B143 Safari/600.1.4 (000648)",
        "Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) CriOS/46.0.2490.73 Mobile/13B143 Safari/600.1.4 (000119)",
        "Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) GSA/9.0.60246 Mobile/13B143 Safari/600.1.4",
        "Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) CriOS/46.0.2490.73 Mobile/13B143 Safari/600.1.4 (000923)",
        "Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) FxiOS/1.2 Mobile/13B143 Safari/601.1.46",
        "Mozilla/5.0 (iPad; CPU OS 9_0 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13A340 Safari/601.1",
        "Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13B143",
        "Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) GSA/10.0.63022 Mobile/13B143 Safari/600.1.4",
        "Mozilla/5.0 (iPad; CPU OS 9_0 like Mac OS X) AppleWebKit/601.1.17 (KHTML, like Gecko) Version/8.0 Mobile/13A175 Safari/600.1.4",
        "Mozilla/5.0 (iPad; CPU OS 9_2 like Mac OS X) AppleWebKit/601.1.56 (KHTML, like Gecko) Version/9.0 Mobile/13c75 Safari/601.1.56",
        "Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B144 Safari/601.1",
        "Mozilla/5.0 (iPad; CPU OS 9_2 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) CriOS/47.0.2526.70 Mobile/13C75 Safari/601.1.46 (000144)",
        "Mozilla/5.0 (iPad; CPU OS 9_2 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) CriOS/47.0.2526.70 Mobile/13C75 Safari/601.1.46 (000042)",
        "Mozilla/5.0 (iPad; CPU OS 9_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13C75 Safari/601.1",
        "Mozilla/5.0 (iPad; CPU OS 7_1_1 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) CriOS/38.0.2125.59 Mobile/11D201 Safari/9537.53",
        "Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) GSA/11.0.65374 Mobile/13B143 Safari/600.1.4",
        "Mozilla/5.0 (iPad; CPU OS 9_2 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) CriOS/47.0.2526.70 Mobile/13C75 Safari/601.1.46 (000468)",
        "Mozilla/5.0 (iPad; CPU OS 9_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) GSA/11.0.65374 Mobile/13C75 Safari/600.1.4",
        "Mozilla/5.0 (iPad; CPU OS 9_0 like Mac OS X) AppleWebKit/601.1.16 (KHTML, like Gecko) Version/8.0 Mobile/13A171a Safari/600.1.4",
        "Mozilla/5.0 (iPad; CPU OS 9_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) GSA/11.1.66360 Mobile/13C75 Safari/600.1.4",
        "Mozilla/5.0 (iPad; CPU OS 9_2 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) CriOS/47.0.2526.83 Mobile/13C75 Safari/601.1.46 (000468)",
        "Mozilla/5.0 (iPad; CPU OS 9_2 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) CriOS/47.0.2526.107 Mobile/13C75 Safari/601.1.46 (000702)",
        "Mozilla/5.0 (iPad; CPU OS 9_0_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/10A403 Safari/601.1",
        "Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B14 3 Safari/601.1",
        "Mozilla/5.0 (iPad; CPU OS 9_2_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13D15 Safari/601.1",
        "Mozilla/5.0 (iPad; CPU OS 9_0_2 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) CriOS/47.0.2526.107 Mobile/13A452 Safari/601.1.46 (000412)",
        "Mozilla/5.0 (iPad; CPU OS 9_2_1 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) CriOS/47.0.2526.107 Mobile/13D15 Safari/601.1.46",
        "Mozilla/5.0 (iPad; CPU OS 9_2_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) GSA/12.0.68608 Mobile/13D15 Safari/600.1.4",
        "Mozilla/5.0 (iPad; CPU OS 9_0_2 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) CriOS/48.0.2564.87 Mobile/13A452 Safari/601.1.46 (000715)",
        "Mozilla/5.0 (iPad; CPU OS 9_2_1 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) CriOS/48.0.2564.87 Mobile/13D15 Safari/601.1.46",
        "Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) CriOS/45.0.2454.89 Mobile/13B143 Safari/600.1.4 (000381)",
        "Mozilla/5.0 (iPad; CPU OS 9_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13E5200d Safari/601.1",
        "Mozilla/5.0 (iPad; CPU OS 9_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13E5200d Safari/601.1",
        "Mozilla/5.0 (iPad; CPU OS 9_2_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) GSA/11.1.66360 Mobile/13D15 Safari/600.1.4",
        "Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) CriOS/48.0.2564.104 Mobile/13B143 Safari/601.1.46",
        "Mozilla/5.0 (iPad; CPU OS 9_2_1 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) CriOS/48.0.2564.104 Mobile/13D15 Safari/601.1.46",
        "Mozilla/5.0 (iPad; CPU OS 9_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13E5200d Safari/601.1.46",
        "Mozilla/5.0 (iPad; CPU OS 9_3 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) CriOS/48.0.2564.104 Mobile/13E5200d Safari/601.1.46",
        "Mozilla/5.0 (iPad; CPU OS 9_2 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) CriOS/47.0.2526.83 Mobile/13C75 Safari/601.1.46",
        "Mozilla/5.0 (iPad; CPU OS 9_2 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) CriOS/47.0.2526.83 Mobile/13C75 Safari/601.1.46 (000381)",
        "Mozilla/5.0 (iPad; CPU OS 9_0 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13A344 Shelter/1.0.0 (YmqLQeAh3Z-nBdz2i87Rf) ",
        "Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) CriOS/46.0.2490.73 Mobile/13C143 Safari/600.1.4 (000718)",
        "Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13A143 Safari/601.1",
        "Mozilla/5.0 (iPad; CPU OS 9_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) FxiOS/1.4 Mobile/13E5181f Safari/601.1.46",
        "Mozilla/5.0 (iPad; CPU OS 9_2_1 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) CriOS/49.0.2623.73 Mobile/13D15 Safari/601.1.46",
        "Mozilla/5.0 (iPad; CPU OS 9_2_1 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) CriOS/49.0.2623.73 Mobile/13A15 Safari/601.1.46",
        "Mozilla/5.0 (iPad; CPU OS 9_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13E233 Safari/601.1",
        "Mozilla/5.0 (iPad; CPU OS 9_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) GSA/13.1.72140 Mobile/13E233 Safari/600.1.4",
        "Mozilla/5.0 (iPad; CPU OS 9_3 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) CriOS/49.0.2623.73 Mobile/13E233 Safari/601.1.46",
        "Mozilla/5.0 (iPad; CPU OS 9_3_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13E238 Safari/601.1",
        "Mozilla/5.0 (iPad; CPU OS 9_3_1 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) CriOS/49.0.2623.109 Mobile/13E238 Safari/601.1.46",
        "Mozilla/5.0 (iPad; CPU OS 9_0_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) FxiOS/1.4 Mobile/13A452 Safari/601.1.46",
        "Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) CriOS/44.0.2403.67 Mobile/13B143 Safari/600.1.4 (000073)",
        "Mozilla/5.0 (iPad; CPU OS 9_3_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) FxiOS/3.0 Mobile/13E238 Safari/601.1.46",
        "Mozilla/5.0 (iPad; CPU OS 9_3_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) GSA/14.1.119979954 Mobile/13E238 Safari/600.1.4",
        "Mozilla/5.0 (iPad; CPU OS 9_3_1 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) CriOS/50.0.2661.95 Mobile/13E238 Safari/601.1.46",
        "Mozilla/5.0 (iPad; CPU OS 9_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13E234 Safari/601.1",
        "Mozilla/5.0 (iPad; CPU OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13F69 Safari/601.1",
        "Mozilla/5.0 (iPad; CPU OS 9_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13E237 Safari/601.1",
        "Mozilla/5.0 (iPad; CPU OS 9_3_2 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) CriOS/50.0.2661.95 Mobile/13F69 Safari/601.1.46",
        "Mozilla/5.0 (iPad; CPU OS 9_3_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) GSA/15.1.122860578 Mobile/13F69 Safari/600.1.4",
        "Mozilla/5.0 (iPad; CPU OS 9_3_2 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) CriOS/51.0.2704.64 Mobile/13F69 Safari/601.1.46",
        "Mozilla/5.0 (iPad; CPU OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13F72 Safari/601.1",
        "Mozilla/5.0 (iPad; CPU OS 9_3_1 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) CriOS/51.0.2704.104 Mobile/13E238 Safari/601.1.46",
        "Mozilla/5.0 (iPad; CPU OS 9_2_1 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) CriOS/50.0.2661.77 Mobile/13D15 Safari/601.1.46",
        "Mozilla/5.0 (iPad; CPU OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) FxiOS/4.0 Mobile/13F69 Safari/601.1.46",
        "Mozilla/5.0 (iPad; CPU OS 9_3_2 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) CriOS/51.0.2704.104 Mobile/13F69 Safari/601.1.46",
        "Mozilla/5.0 (iPad; CPU OS 9_3_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) GSA/16.0.124986583 Mobile/13F69 Safari/600.1.4",
        "Mozilla/5.0 (iPad; CPU OS 9_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) FxiOS/2.0 Mobile/13E5200d Safari/601.1.46",
        "Mozilla/5.0 (iPad; CPU OS 9_3_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13G34 Safari/601.1",
        "Mozilla/5.0 (iPad; CPU OS 9_3_2 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) CriOS/52.0.2743.84 Mobile/13F69 Safari/601.1.46",
        "Mozilla/5.0 (iPad; CPU OS 9_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13E188a Safari/601.1",
        "Mozilla/5.0 (iPad; CPU OS 9_3_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) GSA/17.0.128207670 Mobile/13G35 Safari/600.1.4",
        "Mozilla/5.0 (iPad; CPU OS 9_3_3 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) CriOS/50.0.2661.95 Mobile/13G34 Safari/601.1.46",
        "Mozilla/5.0 (iPad; CPU OS 9_3_4 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13G35 Safari/601.1",
        "Mozilla/5.0 (iPad; CPU OS 9_3_4 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13G35",
        "Mozilla/5.0 (iPad; CPU OS 9_3_4 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) CriOS/52.0.2743.84 Mobile/13G35 Safari/601.1.46",
        "Mozilla/5.0 (iPad; CPU OS 9_3_4 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) FxiOS/5.0 Mobile/13G35 Safari/601.1.46",
        "Mozilla/5.0 (iPad; CPU OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13F69 iPadApp",
        "Mozilla/5.0 (iPad; CPU OS 9_3_4 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13G35 Safari/601.1 MXiOS/4.9.0.60",
        "Mozilla/5.0 (iPad; CPU OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13F69",
        "Mozilla/5.0 (iPad; CPU OS 9_3_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) GSA/18.0.130791545 Mobile/13G35 Safari/600.1.4",
        "Mozilla/5.0 (iPad; CPU OS 9_3_5 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13G36 Safari/601.1",
        "Mozilla/5.0 (iPad; CPU OS 9_3_5 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) GSA/18.0.130791545 Mobile/13G36 Safari/600.1.4",
        "Mozilla/5.0 (iPad; CPU OS 7_1 like Mac OS X) AppleWebKit/537.51.3 (KHTML, like Gecko) Version/7.0 Mobile/11A4149 Safari/9537.72",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36",
        "Mozilla/5.0 (iPad; CPU OS 9_0 like Mac OS X) AppleWebKit/601.1.17 (KHTML, like Gecko) Version/8.0 Mobile/13A175 Safari/600.1.4",
        "Mozilla/5.0 (iPad; CPU OS 9_3_5 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) GSA/18.1.132077863 Mobile/13G36 Safari/600.1.4",
        "Mozilla/5.0 (iPad; CPU OS 9_3_5 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) CriOS/53.0.2785.86 Mobile/13G36 Safari/601.1.46",
        "Mozilla/5.0 (iPad; CPU OS 9_3_2 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) CriOS/53.0.2785.109 Mobile/13F69 Safari/601.1.46",
        "Mozilla/5.0 (iPad; CPU OS 9_3_5 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) CriOS/53.0.2785.109 Mobile/13G36 Safari/601.1.46",
        "Mozilla/5.0 (iPad; CPU OS 9_2 like Mac OSX) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13A452 Safari/601.1",
        "Mozilla/5.0 (iPad; CPU OS 9_2_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13D11",
        "Mozilla/5.0 (iPad; CPU OS 9_3_5 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13G36 Safari/601.1.46 Sleipnir/4.3.0m",
        "Mozilla/5.0 (iPad; CPU OS 9_0_2 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) CriOS/53.0.2785.86 Mobile/13A452 Safari/601.1.46",
        "Mozilla/5.0 (iPad; CPU OS 9_3_5 like Mac OS X) AppleWebKit/601.1.46.140 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1",
        "Mozilla/5.0 (iPad; CPU OS 9_3_5 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) CriOS/54.0.2840.66 Mobile/13G36 Safari/601.1.46",
        "Mozilla/5.0 (iPad; CPU OS 9_3_5 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) CriOS/54.0.2840.91 Mobile/13G36 Safari/601.1.46",
        "Mozilla/5.0 (iPad; CPU OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13F69 Safari/601.1.46 Sleipnir/4.3.2m",
        "Mozilla/5.0 (iPad; CPU OS 9_3_5 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13G36",
        "Mozilla/5.0 (iPad; CPU OS 9_2_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) GSA/5.3.48993 Mobile/13D15 Safari/600.1.4",
        "Mozilla/5.0 (iPad; CPU OS 9_3_1 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) CriOS/54.0.2840.66 Mobile/13E238 Safari/601.1.46",
        "Mozilla/5.0 (iPad; CPU OS 9_3_1 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) CriOS/50.0.2661.77 Mobile/13E238 Safari/601.1.46",
        "Mozilla/5.0 (iPad; CPU OS 9_3_5 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) CriOS/55.0.2883.79 Mobile/13G36 Safari/601.1.46",
        "Mozilla/5.0 (iPad; CPU OS 9_3_2 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) CriOS/55.0.2883.79 Mobile/13F69 Safari/601.1.46",
        "Mozilla/5.0 (iPad; CPU OS 9_3_5 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) FxiOS/5.3 Mobile/13G36 Safari/601.1.46",
        "Mozilla/5.0 (iPad; CPU OS 9_3_5 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) GSA/22.0.141836113 Mobile/13G36 Safari/600.1.4",
        "Mozilla/5.0 (iPad; CPU OS 9_2_1 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) CriOS/56.0.2924.79 Mobile/13D15 Safari/601.1.46",
        "Mozilla/5.0 (iPad; CPU OS 9_3_5 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) CriOS/56.0.2924.79 Mobile/13G36 Safari/601.1.46",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36",
        "Mozilla/5.0 (iPad; CPU OS 9_3_5 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) CriOS/56.0.2924.79 Mobile/13G36 Safari/601.1.46",
        "Mozilla/5.0 (iPad; CPU OS 9_3_5 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) CriOS/57.0.2987.100 Mobile/13G36 Safari/601.1.46",
        "Mozilla/5.0 (iPad; CPU OS 9_2_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) FxiOS/6.1 Mobile/13D15 Safari/601.1.46",
        "Mozilla/5.0 (iPad; CPU OS 9_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13BC75 Safari/601.1",
        "Mozilla/5.0 (iPad; CPU OS 9_3_3 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) CriOS/56.0.2924.79 Mobile/13G34 Safari/601.1.46",
        "Mozilla/5.0 (iPad; CPU OS 9_3_5 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) CriOS/57.0.2987.137 Mobile/13G36 Safari/601.1.46",
        "Mozilla/5.0 (iPad; CPU OS 9_3_5 like Mac OS X) AppleWebKit/601.1.46(KHTML, like Gecko) FxiOS/6.1 Mobile/13G36 Safari/601.1.46",
        "Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25",
        "Mozilla/5.0 (iPad; CPU OS 9_0 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/9.0 Mobile/13A340 Safari/600.1.4",
        "Mozilla/5.0 (iPad; CPU OS 9_3_5 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) CriOS/36.0.1985.49 Mobile/13G36 Safari/9537.53",
        "Mozilla/5.0 (iPad; CPU OS 9_3_5 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) CriOS/59.0.3071.102 Mobile/13G36 Safari/601.1.46"
        ]

def get_header():
    i = random.randint(0,len(user_agent_list)-1)
    headers = {
            'User-Agent': user_agent_list[i],
            'x-forearded-for': "1.2.3.4"
            }
    return headers

def get_multipart_formdata(data, bondary):
    post_data = []
    for key, value in data.iteritems():
        if value is None:
            continue
        post_data.append('--' + bondary )
	post_data.append('Content-Disposition: form-data; name="{0}"'.format(key))
        post_data.append('')
	if isinstance(value, int):
            value = str(value)
        post_data.append(value)
    post_data.append('--' + bondary + '--')
    post_data.append('')
    body = '\r\n'.join(post_data)
    return body.encode('utf-8')

def verify_captcha():
    url = "http://captcha.lianjia.com"
    r = requests.get(url, headers= get_header(), timeout= 30)
    soup = BeautifulSoup(r.content, "lxml")
    pages = soup.find("form", class_="human").find_all("input")
    print pages[2]['value'], pages[2]['name']
    csrf = pages[2]['value']
    time.sleep(1)

    url = "http://captcha.lianjia.com/human"
    r = requests.get(url, headers= get_header(), timeout= 30)
    cookie = r.headers['Set-Cookie']
    soup = BeautifulSoup(r.content, "lxml")
    images = json.loads(r.content)['images']
    uuid = json.loads(r.content)['uuid']

    #print images
    for idx in xrange(0, len(images)):
        fh = open("%d.jpg"%idx, "wb")
        data = images['%d'%idx].split(',', 1)
        fh.write(base64.b64decode(data[1]))
        fh.close()

    step = 0
    mask = 0
    while 1:
        if step == 0:
            val = raw_input("check 0.jpg reverse,(y/n):\t")
            if val == 'y' or val == 'Y':
                mask = mask + 1
            step = 1
        elif step == 1:
            val = raw_input("check 1.jpg reverse,(y/n):\t")
            if val == 'y' or val == 'Y':
                mask = mask + 2
            step = 2
        elif step == 2:
            val = raw_input("check 2.jpg reverse,(y/n):\t")
            if val == 'y' or val == 'Y':
                mask = mask + 4
            step = 3
        elif step == 3:
            val = raw_input("check 3.jpg reverse,(y/n):\t")
            if val == 'y' or val == 'Y':
                mask = mask + 8
            break

    print mask

    boundary='----WebKitFormBoundary7MA4YWxkTrZu0gW'
    headers = get_header()
    headers['content-type'] =  "multipart/form-data; boundary={0}".format(boundary)
    headers['Cookie'] =  cookie
    print get_multipart_formdata({'uuid':uuid, 'bitvalue': mask, '_csrf': csrf}, boundary)
    print headers
    r = requests.post(url, headers=headers, data=get_multipart_formdata({'uuid':uuid, 'bitvalue': mask, '_csrf': csrf}, boundary))

    print r.request
    print r.content


def get_distric_rent_cnt(distric):
    print "try to grab %s community rent cnt "%distric
    url = "http://gz.lianjia.com/zufang/%s/"%distric
    r = requests.get(url, headers= get_header(), timeout= 30)
    #print r.text.encode("utf-8")
    soup = BeautifulSoup(r.content, "lxml")
    pages = soup.find("div", class_="page-box house-lst-page-box")
    time.sleep(random.randint(5,10))
    try:
        pageStr = pages["page-data"]
    except Exception, e:
        print e,r.content
        os._exit(0)
    jo = json.loads(pageStr)
    return jo['totalPage']

def get_distric_community_cnt(distric):
    print "try to grab %s community cnt "%distric
    url = "http://gz.lianjia.com/xiaoqu/%s/"%distric
    r = requests.get(url, headers= get_header(), timeout= 30)
    #print r.text.encode("utf-8")
    soup = BeautifulSoup(r.content, "lxml")
    pages = soup.find("div", class_="page-box house-lst-page-box")
    time.sleep(random.randint(5,10))
    try:
        pageStr = pages["page-data"]
    except Exception, e:
        print e,r.content,r.text
        os._exit(0)
    jo = json.loads(pageStr)
    return jo['totalPage']


def grab_distric(url):
    print "try to grab distric page ", url
    r = requests.get(url, headers= get_header(), timeout= 30)
    soup = BeautifulSoup(r.content, "lxml")

    try:
        districList = soup.find("ul", class_="listContent").find_all('li')
    except Exception, e:
        print e,r.content
        os._exit(0)

    if not districList:
        return

    for item in districList:
        # 房屋详情链接，唯一标识符
        distUrl = item.a["href"] or ''

        #if distUrl in grabedPool["data"]:
        #    print distUrl, "already exits，skip"
        #    continue

        print "start to crawl" , distUrl


        # 抓取 历史成交
        title = item.find("div", class_="title").a.string.encode("utf-8").rstrip()
        historyList = item.find("div", class_="houseInfo").find_all('a')
        history = historyList[0].string.encode("utf-8")
        m = re.match(r"(\d+)天成交(\d+)套", history)
        print m, history
        historyRange = 0
        historySell = 0
        if m:
            historyRange = m.group(1)
            historySell = m.group(2)

        print title, history, historyRange, historySell

        # 抓取 区&商圈
        pos = item.find("div", class_="positionInfo").find_all('a')
        dis = pos[0].string.encode("utf-8")
        bizcircle = pos[1].string.encode("utf-8")
        print dis, bizcircle

        #抓取成交均价噢
        avgStr = item.find("div", class_="totalPrice").span.string.encode("utf-8")
        m = re.match(r"(\d+)", avgStr)
        if m:
            avg = int(avgStr)
        else:
            avg = 0
        print avg

        #抓取在售
        onSell = int(item.find("div", class_="xiaoquListItemSellCount").a.span.string)
        print onSell

        # 通过 ORM 存储到 sqlite
        distItem = DistricHouse(
                                name = title,
                                district = dis,
                                bizcircle = bizcircle,
                                historyRange = historyRange,
                                historySell = historySell,
                                ref = distUrl,
                                avgpx = avg,
                                onsell = onSell,
                                )


        distItem.save()

        # 添加到已经抓取的池
        #grabedPool["data"].add(distUrl)


    # 抓取完成后，休息几秒钟，避免给对方服务器造成大负担
    time.sleep(random.randint(1,3))

def get_distric_chengjiao_cnt(distric, proxy):
    print "try to grab %s chengjiao cnt "%distric
    url = "http://gz.lianjia.com/chengjiao/%s/"%distric
    r = requests.get(url, headers= get_header(), timeout= 30)
    #print r.text.encode("utf-8")
    soup = BeautifulSoup(r.content, "lxml")

    try:
        pages = soup.find("div", class_="page-box house-lst-page-box")
        time.sleep(random.randint(5,10))
        pageStr = pages["page-data"]
        jo = json.loads(pageStr)
        return jo['totalPage']
    except Exception, e:
        print e,r.content
        os._exit(0)

def get_distric_bid_cnt(distric, proxy):
    print "try to grab %s bid cnt "%distric
    url = "http://gz.lianjia.com/ershoufang/%s/"%distric
    r = requests.get(url, headers= get_header(), timeout= 30)
    #print r.text.encode("utf-8")
    soup = BeautifulSoup(r.content, "lxml")

    try:
        pages = soup.find("div", class_="page-box house-lst-page-box")
        time.sleep(random.randint(5,10))
        pageStr = pages["page-data"]
        jo = json.loads(pageStr)
        return jo['totalPage']
    except Exception, e:
        print e,r.content
        os._exit(0)
        #i = random.randint(0,len(proxy)-1)
        #proxies = {
        #        "http": proxy[i]
        #        }
        #print "try proxy", proxy[i]
        #r = requests.get(url, headers= get_header(), proxies=proxies, timeout= 30)
        #soup = BeautifulSoup(r.content, "lxml")
        #pages = soup.find("div", class_="page-box house-lst-page-box")
        #time.sleep(random.randint(5,10))
        #pageStr = pages["page-data"]
        #jo = json.loads(pageStr)
        #return jo['totalPage']

def get_xici_proxy(url, proxys):
    print "get proxy", url
    r = requests.get(url, headers= get_header(), timeout= 10)
    soup = BeautifulSoup(r.content, "lxml")
    pages = soup.find_all("tr", class_="odd")
    for page in pages:
        items = page.find_all("td")
        proxy ="http://%s:%s"%(items[1].string, items[2].string)

        url = "http://gz.lianjia.com/chengjiao/tianhe/"
        proxies = {
                "http": proxy
                }
        try:
            r = requests.get(url, headers= get_header(), proxies=proxies, timeout= 3)
            soup = BeautifulSoup(r.content, "lxml")

            tradedHoustList = soup.find("ul", class_="listContent")
            if not tradedHoustList:
                continue
            proxys.append(proxy)
            print proxy, proxys
        except Exception, e:
            #print Exception,":",e
            continue

def get_kuaidaili_proxy(url, proxys):
    print "get proxy", url
    r = requests.get(url, headers= get_header(), timeout= 10)
    soup = BeautifulSoup(r.content, "lxml")
    pages = soup.find("tbody").find_all("tr")
    for page in pages:
        items = page.find_all("td")
        proxy ="http://%s:%s"%(items[0].string, items[1].string)
        print proxy

        url = "http://gz.lianjia.com/chengjiao/tianhe/"
        proxies = {
                "http": proxy
                }
        try:
            r = requests.get(url, headers= get_header(), proxies=proxies, timeout= 3)
            soup = BeautifulSoup(r.content, "lxml")

            tradedHoustList = soup.find("ul", class_="listContent")
            if not tradedHoustList:
                continue
            proxys.append(proxy)
            print proxy, proxys
        except Exception, e:
            #print Exception,":",e
            continue

def get_youdaili_proxy(url, proxys):
    print "get proxy", url
    r = requests.get(url, headers= get_header(), timeout= 10)
    soup = BeautifulSoup(r.content, "lxml")
    pages = soup.find("div", class_="chunlist").find_all("a")
    page = pages[0]
    u = page["href"]
    html = requests.get(u, headers= get_header(), timeout= 3).content
    proxy_list = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}', html)

    for proxy in proxy_list:
        url = "http://gz.lianjia.com/chengjiao/tianhe/"
        proxies = {
                "http": proxy
                }
        try:
            r = requests.get(url, headers= get_header(), proxies=proxies, timeout= 3)
            soup = BeautifulSoup(r.content, "lxml")

            tradedHoustList = soup.find("ul", class_="listContent")
            if not tradedHoustList:
                continue
            proxys.append(proxy)
            print proxy, proxys
        except Exception, e:
            #print Exception,":",e
            continue

def build_proxy():
    proxys = []
    #get_xici_proxy("http://www.xicidaili.com/nn/1", proxys)
    #get_xici_proxy("http://www.xicidaili.com/nn/2", proxys)

    #get_kuaidaili_proxy("http://www.kuaidaili.com/proxylist/1", proxys)
    #get_kuaidaili_proxy("http://www.kuaidaili.com/proxylist/2", proxys)
    #get_kuaidaili_proxy("http://www.kuaidaili.com/proxylist/3", proxys)
    #get_kuaidaili_proxy("http://www.kuaidaili.com/proxylist/4", proxys)

    #get_youdaili_proxy("http://www.youdaili.net/Daili/http", proxys)

    r = requests.get("http://127.0.0.1:5000/get_all/", headers= get_header(), timeout= 10)
    print r.content
    proxys= json.loads(r.content)
    print proxys

    return proxys


def grabRent(url, proxy, disName, priceDic, bizDic):
    print "try to grab page ", url
    r = requests.get(url, headers= get_header(), timeout= 30)
    soup = BeautifulSoup(r.content, "lxml")
    try:
        bidHoustList = soup.find("ul", class_="house-lst").find_all('li')
    except Exception, e:
        print e,r.content
        os._exit(0)

    if not bidHoustList:
        return

    storge = []
    for item in bidHoustList:
        # 房屋详情链接，唯一标识符
        houseUrl = item.a["href"] or ''


        #if houseUrl in grabedPool["data"]:
        #    print houseUrl, "already exit, skip"
        #    continue

        print 'start to crawl' , houseUrl

        # 抓取 小区，户型，面积 朝向，装修，电梯
	xiaoqu = item.find("div", class_="where").a.string.rstrip().encode("utf-8")
        houseType = item.find("span", class_="zone").span.string.rstrip().encode("utf-8")
        squareStr = item.find("span", class_="meters").string.rstrip().encode("utf-8")
        orientation = item.find("div", class_="where").findAll("span")[4].string.encode("utf-8").rstrip()
        print xiaoqu, houseType, squareStr, orientation

        m = re.match(r"\b[0-9]+(\.[0-9]+)?", squareStr)
        square = 0
        if m:
            square = string.atof(m.group(0))

        print squareStr, square

        #楼层，楼龄
        posInfo = item.find("div", class_="con").contents[2]
        m = re.match(ur"(.*)楼层\(共(\d+)层\)", posInfo)
        floorLevel = 'Nav'
        floorTotal = -1
        if m:
            floorLevel = m.group(1)
            floorTotal = m.group(2)
            print m.group(1).encode("utf-8"), m.group(2)
        print floorLevel.encode("utf-8"), floorTotal

        #挂牌价
        priceInfo = item.find("div", class_="price").span
        if priceInfo:
            price = string.atof(priceInfo.string)
        else :
            price = 0
        print price

        pricePre = item.find("div", class_="price-pre").string
        priceUpdate, misc = ([x.strip() for x in pricePre.split(" ")])
        print priceUpdate


        #关注，带看， 放盘
        seenStr = item.find("div", class_="square").find("span", class_="num").string
        seen = 0
        if m:
            seen = string.atoi(seenStr)
        print seen


        try:
            avg = priceDic[xiaoqu]
        except Exception, e:
            print e
            avg = 0
        print "avg", avg

        try:
            biz = bizDic[xiaoqu]
        except Exception, e:
            print e
            biz = ""
        print "biz", biz


        loan = 0
        loan = square*avg -1500000

        loanRet = 0
        yearRate = 0.049
        monthRate = 0.049/12
        loanYear = 30
        loanMonth = loanYear*12

        if loan < 0 :
            loan = 0
            loanRet = 0
        else:
            loanRet = loan*monthRate*((1+monthRate)**loanMonth)/(((1+monthRate)**loanMonth)-1)
            loan = round(loan/10000)
        print loan, loanRet


        # 通过 ORM 存储到 sqlite
        BidItem = RentHouse(
                                xiaoqu = xiaoqu,
                                houseType = houseType,
                                square = square,
                                houseUrl = houseUrl,
                                orientation = orientation,
                                floorLevel = floorLevel,
                                floorTotal = floorTotal,
                                price = price,
                                avg = avg,
                                loan = loan,
                                loanRet = loanRet,
                                seen = seen,
                                bizcircle = biz,
                                district = disName,
                                )

        storge.append(BidItem)


    for s in storge:
        s.save()
        # 添加到已经抓取的池
        #grabedPool["data"].add(s.houseUrl)

    # 抓取完成后，休息几秒钟，避免给对方服务器造成大负担
    time.sleep(random.randint(1,3))

def grabBid(url, proxy, disName, priceDic):
    print "try to grabbid page ", url
    r = requests.get(url, headers= get_header(), timeout= 30)
    soup = BeautifulSoup(r.content, "lxml")
    try:
        bidHoustList = soup.find("ul", class_="sellListContent").find_all('li')
    except Exception, e:
        print e,r.content
        os._exit(0)
        i = random.randint(0,len(proxy)-1)
        proxies = {
                "http": proxy[i]
                }
        print "try proxy", proxy[i]
        r = requests.get(url, headers= get_header(), proxies=proxies, timeout= 30)
        soup = BeautifulSoup(r.content, "lxml")
        bidHoustList = soup.find("ul", class_="sellListContent").find_all('li')

    if not bidHoustList:
        return

    storge = []
    for item in bidHoustList:
        # 房屋详情链接，唯一标识符
        houseUrl = item.a["href"] or ''


        #if houseUrl in grabedPool["data"]:
        #    print houseUrl, "already exit, skip"
        #    continue

        print 'start to crawl' , houseUrl

        # 抓取 小区，户型，面积 朝向，装修，电梯
        houseInfo = item.find("div", class_="houseInfo").contents[2]
        xiaoqu = item.find("div", class_="houseInfo").a.string.encode("utf-8").rstrip()
        if houseInfo:
            if len(houseInfo.split("|")) == 5:
                null, houseType, squareStr, orientation, decoration = ([x.strip() for x in houseInfo.split("|")])
                elevator = 'Nav'
            if len(houseInfo.split("|")) == 6:
                null, houseType, squareStr, orientation, decoration, elevator = ([x.strip() for x in houseInfo.split("|")])
        print xiaoqu, houseType.encode("utf-8"), orientation.encode("utf-8"), decoration.encode("utf-8"), elevator.encode("utf-8")

        m = re.match(ur"\b[0-9]+(\.[0-9]+)?", squareStr)
        square = 0
        if m:
            square = string.atof(m.group(0))

        print squareStr.encode("utf-8"), square

        #楼层，楼龄
        posInfo = item.find("div", class_="positionInfo").contents[1]
        print posInfo.encode("utf-8")
        m = re.match(ur"(.*)楼层\(共(\d+)层\)(\d+)年建", posInfo)
        floorLevel = 'Nav'
        floorTotal = -1
        build = -1
        if m:
            floorLevel = m.group(1)
            floorTotal = m.group(2)
            build = int(m.group(3))
            print m.group(1).encode("utf-8"), m.group(2), m.group(3)
        print floorLevel.encode("utf-8"), floorTotal, build

        biz = item.find("div", class_="positionInfo").a.string
        print biz

        #挂牌价
        priceInfo = item.find("div", class_="totalPrice").span
        if priceInfo:
            bid = string.atof(priceInfo.string)
        else :
            bid = 0
        print bid


        #均价
        priceInfo = item.find("div", class_="unitPrice").span
        priceStr = ""
        if priceInfo:
            priceStr = priceInfo.string
        m = re.match(ur"单价(\d+)元", priceStr)
        price = 0
        if m:
            price = m.group(1)

        print price, priceStr.encode("utf-8")

        #关注，带看， 放盘
        followInfo = item.find("div", class_="followInfo").contents[1]
        if followInfo:
            watchStr, seenStr, releaseStr = ([x.strip() for x in followInfo.split("/")])
        print watchStr.encode("utf-8"), seenStr.encode("utf-8"), releaseStr.encode("utf-8")
        m = re.match(ur"(\d+)人", watchStr)
        watch = 0
        if m:
            watch = m.group(1)

        m = re.match(ur"共(\d+)次", seenStr)
        seen = 0
        if m:
            seen = m.group(1)

        m = re.match(ur"(\d+)天", releaseStr)
        release = 0
        if m:
            release = int(m.group(1))
        else:
            m = re.match(ur"(\d+)个月", releaseStr)
            if m:
                release = int(m.group(1))*30
            else:
                m = re.match(ur"(.*)年", releaseStr)
                if m:
                    release = m.group(1)
                    if release == u"一":
                        release = 365

        try:
            avg = priceDic[xiaoqu]
        except Exception, e:
            avg = 0
        print watch, seen, release, avg

        # 通过 ORM 存储到 sqlite
        BidItem = BidHouse(
                                xiaoqu = xiaoqu,
                                houseType = houseType,
                                square = square,
                                houseUrl = houseUrl,
                                orientation = orientation,
                                decoration = decoration,
                                elevator = elevator,
                                floorLevel = floorLevel,
                                floorTotal = floorTotal,
                                build = build,
                                price = price,
                                avg = avg,
                                bid = bid,
                                watch = watch,
                                seen = seen,
                                release = release,
                                bizcircle = biz,
                                district = disName,
                                )

        storge.append(BidItem)


    for s in storge:
        s.save()
        # 添加到已经抓取的池
        #grabedPool["data"].add(s.houseUrl)

    # 抓取完成后，休息几秒钟，避免给对方服务器造成大负担
    time.sleep(random.randint(1,3))

def grab(url, proxy, disName, bizDic, lastMarkTrade):
    print "try to grab page ", url
    r = requests.get(url, headers= get_header(), timeout= 30)
    soup = BeautifulSoup(r.content, "lxml")
    try:
        tradedHoustList = soup.find("ul", class_="listContent").find_all('li')
    except Exception, e:
        print e,r.content
        #os._exit(0)

        tradedHoustList = soup.find("li", class_="pictext")
        if not tradedHoustList:
            tradedHoustList = soup.find("ul", class_="listContent").find_all('li')
        else:
            i = random.randint(0,len(proxy)-1)
            proxies = {
                "http": proxy[i]
                }
            print "try proxy", proxy[i]
            r = requests.get(url, headers= get_header(), proxies=proxies, timeout= 30)
            soup = BeautifulSoup(r.content, "lxml")
            tradedHoustList = soup.find("ul", class_="listContent").find_all('li')

    if not tradedHoustList:
        return

    storge = []
    stop = False
    for item in tradedHoustList:
        # 房屋详情链接，唯一标识符
        houseUrl = item.a["href"] or ''


        #if houseUrl in grabedPool["data"]:
        #    print houseUrl, "already exit, skip"
        #    continue

        print 'start to crawl' , houseUrl


        # 抓取 小区，户型，面积
        title = item.find("div", class_="title")
        if title:
            print title
            xiaoqu, houseType, square = (title.string.replace("  ", " ").split(" "))
            m = re.match(ur"\b[0-9]+(\.[0-9]+)?", square)
            if m:
                square = string.atof(m.group(0))
        else:
            xiaoqu, houseType, square = ('Nav', 'Nav', 0)

        xiaoqu = xiaoqu.encode("utf-8").rstrip()
        houseType = houseType.encode("utf-8")
        print xiaoqu, houseType, square

        dealInfo = item.find("div", class_="totalPrice").span
        try:
            deal = string.atof(dealInfo.string.encode("utf-8"))
        except Exception, e:
            deal = -1
        print deal

        # 朝向，装修，电梯
        houseInfo = item.find("div", class_="houseInfo").contents[1]
        if houseInfo:
            if len(houseInfo.split("|")) == 2:
                orientation, decoration = ([x.strip() for x in houseInfo.split("|")])
                elevator = 'Nav'
            if len(houseInfo.split("|")) == 3:
                orientation, decoration, elevator = ([x.strip() for x in houseInfo.split("|")])
        print orientation.encode("utf-8"), decoration.encode("utf-8"), elevator.encode("utf-8")

        #成交日期
        dealDate = item.find("div", class_="dealDate")
        if dealDate:
            tradeDate = datetime.datetime.strptime(dealDate.string, '%Y.%m.%d') or datetime.datetime(1990, 1, 1)
        print tradeDate
        if lastMarkTrade >= tradeDate:
            print 'break for time'
            stop = True
            break

        #楼层，楼龄
        posInfo = item.find("div", class_="positionInfo").contents[1]
        if posInfo:
            floor, buildStr = ([x.strip() for x in posInfo.split(" ")])
        print floor.encode("utf-8"), buildStr.encode("utf-8")
        m = re.match(ur"(.*)楼层\(共(\d+)层\)", floor)
        floorLevel = 'Nav'
        floorTotal = -1
        if m:
            floorLevel = m.group(1)
            floorTotal = m.group(2)
            print m.group(1).encode("utf-8"), m.group(2)
        m = re.match(ur"(\d+)年建", buildStr)
        build = -1
        if m:
            build = m.group(1)
        print floorLevel.encode("utf-8"), floorTotal, build

        #均价
        priceInfo = item.find("div", class_="unitPrice").span
        if priceInfo:
            price = int(priceInfo.string)
        else :
            price = 0
        print price

        #挂牌价，成交周期
        dealCycle = item.find("span", class_="dealCycleTxt").find_all('span')
        bid = -1
        cycle = -1
        if dealCycle:
            if len(dealCycle) == 1:
                bidStr = dealCycle[0].string
                cycleStr = ""

            if len(dealCycle) == 2:
                bidStr = dealCycle[0].string
                cycleStr = dealCycle[1].string

            print bidStr.encode("utf-8"), cycleStr.encode("utf-8")
            m = re.match(ur"挂牌(\d+)万", bidStr)
            if m:
                bid = m.group(1)

            m = re.match(ur"成交周期(\d+)天", cycleStr)
            if m:
                cycle = m.group(1)

        try:
            biz = bizDic[xiaoqu]
        except Exception, e:
            biz = "unknown"
        #print bid, cycle, disName, biz

        # 通过 ORM 存储到 sqlite
        tradeItem = TradedHouse(
                                xiaoqu = xiaoqu,
                                houseType = houseType,
                                square = square,
                                houseUrl = houseUrl,
                                orientation = orientation,
                                decoration = decoration,
                                elevator = elevator,
                                floorLevel = floorLevel,
                                floorTotal = floorTotal,
                                build = build,
                                price = price,
                                tradeDate = tradeDate,
                                bid = bid,
                                deal = deal,
                                cycle = cycle,
                                district = disName,
                                bizcircle = biz,
                                )

        storge.append(tradeItem)


    for s in storge:
        s.save()
        # 添加到已经抓取的池
        #grabedPool["data"].add(s.houseUrl)

    # 抓取完成后，休息几秒钟，避免给对方服务器造成大负担
    time.sleep(random.randint(1,3))
    return stop

step_context = {"phase":0, "cnt":0, "offset":0, "pgoffset":1, "date":"20170705"}

def save_context():
    global step_context
    print "save", step_context, type(step_context)
    json.dump(step_context, open('context','w'))

def load_context():
    global step_context
    step_context = json.load(open('context','r'))
    print "load", step_context, type(step_context)


def crawl_district():
    global step_context
    for dis_offset in xrange(step_context['offset'], len(gz_district)):
        dis = gz_district[dis_offset]
        step_context['offset'] = dis_offset
        save_context()

        cnt = step_context['cnt']
        if cnt == 0:
            cnt = get_distric_community_cnt(dis)
        print "get_distric_info", dis, cnt
        step_context['cnt'] = cnt
        save_context()
        for i in xrange(step_context['pgoffset'], cnt+1):
            step_context['pgoffset'] = i
            save_context()
            url = "http://gz.lianjia.com/xiaoqu/%s/pg%s/"%(dis, format(str(i)))
            grab_distric(url)
        step_context['pgoffset'] = 1
        step_context['cnt'] = 0
        save_context()

def crawl_district_chengjiao():
    global step_context
    for dis_offset in xrange(step_context['offset'], len(gz_district)):
        dis = gz_district[dis_offset]
        step_context['offset'] = dis_offset
        save_context()

        distric = DistricHouse.select(DistricHouse.name, DistricHouse.bizcircle, DistricHouse.avgpx).where(DistricHouse.district == gz_district_name[dis])
        print distric
        bizDic = {}
        priceDic = {}
        for item in distric:
            name = item.name.rstrip().encode("utf-8")
            biz = item.bizcircle.encode("utf-8")
            bizDic[name] = biz
            price = item.avgpx
            priceDic[name] = price
            #print name

        cnt = step_context['cnt']
        if cnt == 0:
            cnt = get_distric_chengjiao_cnt(dis, [])

        step_context['cnt'] = cnt
        save_context()

        ts = TradedHouse.select(TradedHouse.tradeDate).where(TradedHouse.district == gz_district_name[dis]).order_by(TradedHouse.tradeDate.desc()).limit(1)
        print ts
        for item in ts:
            print item.tradeDate, type(item.tradeDate)
            lastMarkTrade = item.tradeDate

        for i in xrange(step_context['pgoffset'], cnt+1):
            step_context['pgoffset'] = i
            save_context()
            page = "http://gz.lianjia.com/chengjiao/%s/pg%s/"%(dis, format(str(i)))
            stop = grab(page, [], gz_district_name[dis], bizDic, lastMarkTrade)
            if stop == True:
                break

        step_context['pgoffset'] = 1
        step_context['cnt'] = 0
        save_context()

def crawl_district_bid():
    global step_context
    #proxy = build_proxy()
    for dis_offset in xrange(step_context['offset'], len(gz_district)):
        dis = gz_district[dis_offset]
        distric = DistricHouse.select(DistricHouse.name, DistricHouse.bizcircle, DistricHouse.avgpx).where(DistricHouse.district == gz_district_name[dis])
        print distric
        bizDic = {}
        priceDic = {}
        for item in distric:
            name = item.name.rstrip().encode("utf-8")
            biz = item.bizcircle.encode("utf-8")
            bizDic[name] = biz
            price = item.avgpx
            priceDic[name] = price
            #print name

        step_context['offset'] = dis_offset
        save_context()

        cnt = step_context['cnt']
        if cnt == 0:
            cnt = get_distric_bid_cnt(dis, [])

        step_context['cnt'] = cnt
        save_context()
        for i in xrange(step_context['pgoffset'], cnt+1):
            step_context['pgoffset'] = i
            save_context()
            page = "http://gz.lianjia.com/ershoufang/%s/pg%s/"%(dis, format(str(i)))
            grabBid(page, [], gz_district_name[dis], priceDic)

        step_context['pgoffset'] = 1
        step_context['cnt'] = 0
        save_context()

def crawl_district_rent():
    global step_context
    for dis_offset in xrange(step_context['offset'], len(gz_district)):
        dis = gz_district[dis_offset]
        distric = DistricHouse.select(DistricHouse.name, DistricHouse.bizcircle, DistricHouse.avgpx).where(DistricHouse.district == gz_district_name[dis])
        print distric
        bizDic = {}
        priceDic = {}
        for item in distric:
            name = item.name.rstrip().encode("utf-8")
            biz = item.bizcircle.encode("utf-8")
            bizDic[name] = biz
            price = item.avgpx
            priceDic[name] = price
            #print name

        step_context['offset'] = dis_offset
        save_context()

        cnt = step_context['cnt']
        if cnt == 0:
            cnt = get_distric_rent_cnt(dis)

        step_context['cnt'] = cnt
        save_context()
        for i in xrange(step_context['pgoffset'], cnt+1):
            step_context['pgoffset'] = i
            save_context()
            page = "http://gz.lianjia.com/zufang/%s/pg%s/"%(dis, format(str(i)))
            grabRent(page, [], gz_district_name[dis], priceDic, bizDic)

        step_context['pgoffset'] = 1
        step_context['cnt'] = 0
        save_context()


def process_context():
    #global step_context
    print step_context['phase']
    if step_context['phase'] == 0:
        crawl_district()
        step_context['phase'] = 1
        step_context['cnt'] = 0
        step_context['offset'] = 0
        step_context['pgoffset'] = 1
        step_context['date'] = time.strftime("%Y%m%d", time.localtime())
        save_context()
    elif step_context['phase'] == 1:
        crawl_district_chengjiao()
        step_context['phase'] = 2
        step_context['cnt'] = 0
        step_context['offset'] = 0
        step_context['pgoffset'] = 1
        save_context()
    elif step_context['phase'] == 2:
        crawl_district_bid()
        step_context['phase'] = 3
        step_context['cnt'] = 0
        step_context['offset'] = 0
        step_context['pgoffset'] = 1
        save_context()
    elif step_context['phase'] == 3:
        crawl_district_rent()
        step_context['phase'] = -1
        step_context['cnt'] = 0
        step_context['offset'] = 0
        step_context['pgoffset'] = 1
        save_context()
    elif step_context['phase'] == -1:
        #shutil.copy('houseprice.db', time.strftime("houseprice_%Y%m%d.db", time.localtime()))
        clear_table()
        step_context['phase'] = 1

if __name__== "__main__":
    #save_context()
    load_context()
    #verify_captcha()

    if step_context['phase'] == -1:
        process_context()

    while step_context['phase'] != -1:
        process_context()
