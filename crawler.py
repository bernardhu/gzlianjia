# -*- coding: utf-8 -*-

import pickle
import os.path
import datetime
import time
import random
import json
import re
import chardet


import requests
from bs4 import BeautifulSoup


from model import TradedHouse, DistricHouse


grabedPool = {}

#gz_district = ['tianhe', 'yuexiu', 'liwan', 'panyu', 'baiyun', 'huangpugz', 'conghua', 'zengcheng', 'huadou', 'luogang', 'nansha']
gz_district = ['nansha']
global start_offset
start_offset = 4


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

def before_grab(func):
    def wapper(*args, **kwargs):
        if os.path.exists("grabedPool.set"):
            with open("grabedPool.set", "rb") as f:
                grabedPool["data"] = pickle.load(f)
        else:
            grabedPool["data"] = set([])

        func(*args, **kwargs)
    return wapper


def after_grab(func):
    def wapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception, e:
            raise
        finally:
            with open("grabedPool.set" , "wb") as f:
                pickle.dump(grabedPool["data"], f)
    return wapper

def get_distric_community_cnt(distric):
    print "try to grab %s community cnt "%distric
    url = "http://gz.lianjia.com/xiaoqu/%s/"%distric
    r = requests.get(url, headers= get_header(), timeout= 30)
    print r.text
    soup = BeautifulSoup(r.content, "lxml")
    pages = soup.find("div", class_="page-box house-lst-page-box")
    time.sleep(random.randint(5,10))
    pageStr = pages["page-data"]
    jo = json.loads(pageStr)
    return jo['totalPage']

def get_distric_info(distric, cnt):
    global start_offset
    for i in xrange(start_offset, cnt):
        url = "http://gz.lianjia.com/xiaoqu/%s/pg%s/"%(distric, format(str(i)))
        grab_distric(url)
    if start_offset > 1:
        start_offset = 1

def grab_distric(url):
    print "try to grab distric page ", url
    r = requests.get(url, headers= get_header(), timeout= 30)
    soup = BeautifulSoup(r.content, "lxml")

    districList = soup.find("ul", class_="listContent").find_all('li')
    if not districList:
        return

    for item in districList:
        # 房屋详情链接，唯一标识符
        distUrl = item.a["href"] or ''

        if distUrl in grabedPool["data"]:
            print distUrl, " 已经存在，跳过，开始抓取下一个"
            continue

        print '开始抓取' , distUrl


        # 抓取 历史成交
        title = item.find("div", class_="title").a.string
        historyList = item.find("div", class_="houseInfo").find_all('a')
        history = historyList[0].string
        m = re.match(ur"(\d+)天成交(\d+)套", history)
        print m, history
        historyRange = 0
        historySell = 0
        if m:
            historyRange = m.group(1)
            historySell = m.group(2)

        print title, history, historyRange, historySell

        # 抓取 区&商圈
        pos = item.find("div", class_="positionInfo").find_all('a')
        dis = pos[0].string
        bizcircle = pos[1].string
        print dis, bizcircle

        #抓取成交均价噢
        avgStr = item.find("div", class_="totalPrice").span.string
        m = re.match(ur"(\d+)", avgStr)
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
        grabedPool["data"].add(distUrl)


    # 抓取完成后，休息几秒钟，避免给对方服务器造成大负担
    time.sleep(random.randint(1,3))

def get_distric_chengjiao_cnt(distric, proxy):
    print "try to grab %s chengjiao cnt "%distric
    url = "http://gz.lianjia.com/chengjiao/%s/"%distric
    r = requests.get(url, headers= get_header(), timeout= 30)
    soup = BeautifulSoup(r.content, "lxml")

    try:
        pages = soup.find("div", class_="page-box house-lst-page-box")
        time.sleep(random.randint(5,10))
        pageStr = pages["page-data"]
        jo = json.loads(pageStr)
        return jo['totalPage']
    except Exception, e:
        i = random.randint(0,len(proxy)-1)
        proxies = {
                "http": proxy[i]
                }
        print "try proxy", proxy[i]
        r = requests.get(url, headers= get_header(), proxies=proxies, timeout= 30)
        soup = BeautifulSoup(r.content, "lxml")
        pages = soup.find("div", class_="page-box house-lst-page-box")
        time.sleep(random.randint(5,10))
        pageStr = pages["page-data"]
        jo = json.loads(pageStr)
        return jo['totalPage']

def get_xici_proxy(url, proxys):
    r = requests.get(url, headers= get_header(), timeout= 30)
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
            r = requests.get(url, headers= get_header(), proxies=proxies, timeout= 10)
            soup = BeautifulSoup(r.content, "lxml")

            tradedHoustList = soup.find("ul", class_="listContent")
            if not tradedHoustList:
                continue
            proxys.append(proxy)
            print proxy
        except Exception, e:
            print Exception,":",e

def get_kuaidaili_proxy(url, proxys):
    r = requests.get(url, headers= get_header(), timeout= 30)
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
            r = requests.get(url, headers= get_header(), proxies=proxies, timeout= 10)
            soup = BeautifulSoup(r.content, "lxml")

            tradedHoustList = soup.find("ul", class_="listContent")
            if not tradedHoustList:
                continue
            proxys.append(proxy)
            print proxy
        except Exception, e:
            print Exception,":",e

def get_youdaili_proxy(url, proxys):
    r = requests.get(url, headers= get_header(), timeout= 30)
    soup = BeautifulSoup(r.content, "lxml")
    pages = soup.find("div", class_="chunlist").find_all("a")
    page = pages[0]
    u = page["href"]
    html = requests.get(u, headers= get_header(), timeout= 30).content
    proxy_list = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}', html)

    for proxy in proxy_list:
        url = "http://gz.lianjia.com/chengjiao/tianhe/"
        proxies = {
                "http": proxy
                }
        try:
            r = requests.get(url, headers= get_header(), proxies=proxies, timeout= 10)
            soup = BeautifulSoup(r.content, "lxml")

            tradedHoustList = soup.find("ul", class_="listContent")
            if not tradedHoustList:
                continue
            proxys.append(proxy)
            print proxy
        except Exception, e:
            print Exception,":",e

def build_proxy():
    proxys = []
    get_xici_proxy("http://www.xicidaili.com/nn/1", proxys)
    get_xici_proxy("http://www.xicidaili.com/nn/2", proxys)

    get_kuaidaili_proxy("http://www.kuaidaili.com/proxylist/1", proxys)
    get_kuaidaili_proxy("http://www.kuaidaili.com/proxylist/2", proxys)
    get_kuaidaili_proxy("http://www.kuaidaili.com/proxylist/3", proxys)
    get_kuaidaili_proxy("http://www.kuaidaili.com/proxylist/4", proxys)

    get_youdaili_proxy("http://www.youdaili.net/Daili/http", proxys)

    print proxys


@before_grab
def start():
    #build_proxy()
    for dis in gz_district:
        cnt = get_distric_community_cnt(dis)
        get_distric_info(dis, cnt)

    proxy = [
            'http://222.85.50.165:808',
            'http://119.5.1.96:808',
            'http://115.220.147.11:808',
            'http://123.179.131.32:8080',
            'http://175.155.25.55:808',
            'http://183.32.88.169:808',
            'http://222.85.39.168:808',
            'http://183.32.89.7:808',
            'http://222.139.197.72:8118',
            'http://222.179.210.94:8081',
            'http://119.90.63.3:3128',
            'http://113.123.39.222:808',
            'http://58.52.201.117:8080',
            'http://103.238.202.103:8080',
            'http://210.22.85.34:8080']
    global start_offset
    for dis in gz_district:
        cnt = get_distric_chengjiao_cnt(dis, proxy)
        for i in xrange(start_offset, cnt+1):
            page = "http://gz.lianjia.com/chengjiao/%s/pg%s/"%(dis, format(str(i)))
            #grab(page, proxy)

        if start_offset > 1:
            start_offset = 1


@after_grab
def grab(url, proxy):
    print "try to grab page ", url
    r = requests.get(url, headers= get_header(), timeout= 30)
    soup = BeautifulSoup(r.content, "lxml")
    try:
        tradedHoustList = soup.find("ul", class_="listContent").find_all('li')
    except Exception, e:
        i = random.randint(0,len(proxy)-1)
        proxies = {
                "http": proxy[i]
                }
        print "try proxy", proxy[i]
        r = requests.get(url, headers= get_header(), proxies=proxies, timeout= 10)
        soup = BeautifulSoup(r.content, "lxml")
        tradedHoustList = soup.find("ul", class_="listContent").find_all('li')

    if not tradedHoustList:
        return

    for item in tradedHoustList:
        # 房屋详情链接，唯一标识符
        houseUrl = item.a["href"] or ''


        if houseUrl in grabedPool["data"]:
            print houseUrl, " 已经存在，跳过，开始抓取下一个"
            continue

        print '开始抓取' , houseUrl


        # 抓取 小区，户型，面积
        title = item.find("div", class_="title")
        if title:
            print title
            xiaoqu, houseType, square = (title.string.replace("  ", " ").split(" "))
            m = re.match(ur'\b[0-9]+(\.[0-9]+)?', square)
            if m:
                square = m.group(1)
        else:
            xiaoqu, houseType, square = ('Nav', 'Nav', 0)
        print xiaoqu, houseType, square

        deal = int(item.find("div", class_="totalPrice").span.string)
        print deal

        # 朝向，装修，电梯
        houseInfo = item.find("div", class_="houseInfo").contents[1]
        if houseInfo:
            if len(houseInfo.split("|")) == 2:
                orientation, decoration = ([x.strip() for x in houseInfo.split("|")])
                elevator = 'Nav'
            if len(houseInfo.split("|")) == 3:
                orientation, decoration, elevator = ([x.strip() for x in houseInfo.split("|")])
        print orientation, decoration, elevator

        #成交日期
        dealDate = item.find("div", class_="dealDate")
        if dealDate:
            tradeDate = datetime.datetime.strptime(dealDate.string, '%Y.%m.%d') or datetime.datetime(1990, 1, 1)
        print tradeDate

        #楼层，楼龄
        posInfo = item.find("div", class_="positionInfo").contents[1]
        if posInfo:
            floor, build = ([x.strip() for x in posInfo.split(" ")])
        m = re.match(ur'(\w+)楼层(共(\d+)层)', floor)
        if m:
            floorLevel = m.group(1)
            floorTotal = m.group(2)
        m = re.match(r'(\d+)年建', build)
        if m:
            build = m.group(1)
        print floorLevel, floorTotal, build

        #均价
        priceInfo = item.find("div", class_="unitPrice").span
        if priceInfo:
            price = int(priceInfo.string)
        else :
            price = 0
        print price

        #挂牌价，成交周期
        dealCycle = item.find("span", class_="dealCycleTxt").find_all('span')
        if dealCycle:
            if len(dealCycle) == 1:
                bid = int(dealCycle[0].string)
                cycle = 0

            if len(dealCycle) == 2:
                bid = int(dealCycle[0].string)
                cycle = int(dealCycle[1].string)
        print bid, cycle

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
                                )


        tradeItem.save()

        # 添加到已经抓取的池
        grabedPool["data"].add(houseUrl)


    # 抓取完成后，休息几秒钟，避免给对方服务器造成大负担
    time.sleep(random.randint(1,3))


if __name__== "__main__":
    start()
