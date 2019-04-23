#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from selenium import webdriver

baseurl = "http://www.fynas.com/ua/search?d=&b=&k=&page="

browser = webdriver.Chrome('./chromedriver73')

list = []



def getInfo(page):
    u = baseurl + str(page)
    browser.get(u)
    tbody = browser.find_element_by_tag_name('tbody')
    trs = tbody.find_elements_by_tag_name("tr")
    isFirst = True
    for tr in trs:
        if isFirst:
            isFirst = False
            continue
        # tr是一行
        tds = tr.find_elements_by_tag_name("td")
        shouji = tds[0].find_element_by_tag_name("a").text
        jixing = tds[1].text
        liulanqi = tds[2].text
        ua = tds[3].text
        list.append((shouji, jixing, liulanqi, ua))


for i in range(1, 11):
    print(i)
    getInfo(i)

browser.close()
# print(list)
with open('./log.log', 'w') as w:
    for tr in list:
        for td in tr:
            w.write(str(td) + '\n')
