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
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"
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
    headers = {'content-type': "multipart/form-data; boundary={0}".format(boundary)}
    r = requests.post(url, headers=headers, data=get_multipart_formdata({'uuid':uuid, 'bitvalue': mask, '_csrf': csrf}, boundary))
    print get_multipart_formdata({'uuid':uuid, 'bitvalue': mask, '_csrf': csrf}, boundary)

    print r.request


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

    get_kuaidaili_proxy("http://www.kuaidaili.com/proxylist/1", proxys)
    get_kuaidaili_proxy("http://www.kuaidaili.com/proxylist/2", proxys)
    get_kuaidaili_proxy("http://www.kuaidaili.com/proxylist/3", proxys)
    get_kuaidaili_proxy("http://www.kuaidaili.com/proxylist/4", proxys)

    #get_youdaili_proxy("http://www.youdaili.net/Daili/http", proxys)

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
    print "try to grab page ", url
    r = requests.get(url, headers= get_header(), timeout= 30)
    soup = BeautifulSoup(r.content, "lxml")
    try:
        bidHoustList = soup.find("ul", class_="sellListContent").find_all('li')
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

def grab(url, proxy, disName, bizDic):
    print "try to grab page ", url
    r = requests.get(url, headers= get_header(), timeout= 30)
    soup = BeautifulSoup(r.content, "lxml")
    try:
        tradedHoustList = soup.find("ul", class_="listContent").find_all('li')
    except Exception, e:
        print e,r.content
        os._exit(0)

    if not tradedHoustList:
        return

    storge = []
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
        if dealInfo:
            deal = string.atof(dealInfo.string.encode("utf-8"))
        else :
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
        print bid, cycle, disName, biz

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
        for i in xrange(step_context['pgoffset'], cnt+1):
            step_context['pgoffset'] = i
            save_context()
            page = "http://gz.lianjia.com/chengjiao/%s/pg%s/"%(dis, format(str(i)))
            grab(page, [], gz_district_name[dis], bizDic)

        step_context['pgoffset'] = 1
        step_context['cnt'] = 0
        save_context()

def crawl_district_bid():
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
