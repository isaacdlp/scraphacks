#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
from selenium import webdriver

from browsermobproxy import Server
import time
import collections
import os
import shutil
import json

import sys
sys.path.append('./pdfreactor/')
from PDFreactor import *


courses = [
    "https://www.safaribooksonline.com/library/view/python-data-structures/9781786467355/"
    # "https://www.safaribooksonline.com/topics/python",
    # "https://www.safaribooksonline.com/library/view/practical-python-data/9781788294294/",
    # "https://www.safaribooksonline.com/library/view/numpy-cookbook/9781849518925/",
]

overwrite = False
topicNum = 0

pdfReactor = None
# pdfReactor = PDFreactor("http://localhost:9423/service/rest")


def cuteprint(text):
    print(text.encode(sys.stdout.encoding, 'ignore'))

def cleanName(name):
    max = 100
    pre = "".join([c for c in name if c.isalpha() or c.isdigit() or c == ' ']).rstrip().replace(' ', '_')
    if len(pre) > max:
        pre = pre[0:max]
    return pre

def listChapters(main, prior, dlist):
    cur = 0
    children = main.find_elements_by_xpath("./li")
    for child in children:
        cur += 1
        urior = str(cur)
        if prior != "":
            urior = "%s_%s" % (prior, urior)
        try:
            link = child.find_element_by_xpath("./a")

            name = "%s-%s" % (urior, cleanName(link.text))
            dlist[name] = link.get_attribute("href")
            # cuteprint(name)
        except:
            pass

        nodes = child.find_elements_by_xpath("./ol")
        for node in nodes:
            listChapters(node, urior, dlist)

def doCourse(course):
    global overwrite

    if "/topics/" in course:
        doTopic(course)
    else:
        driver.get(course)

        title = cleanName(driver.find_element_by_css_selector("h1.t-title").text)
        cuteprint("- - -")
        cuteprint(title)
        cuteprint("- - -")

        folder = "%s/%s" % ("safari", title)
        try:
            created = False
            if not os.path.exists(folder):
                os.mkdir(folder)
                created = True
            else:
                cuteprint("ALREADY EXISTS")

            if created or overwrite:
                desc = driver.find_element_by_class_name("t-description")

                toc = driver.find_element_by_class_name("detail-toc")
                dlist = collections.OrderedDict()
                listChapters(toc, "", dlist)

                with open("%s/0_Description.html" % (folder), "w", encoding="utf8") as book:
                    book.write('<html><head><meta charset="UTF-8"/></head><body>')
                    book.write("<div>%s</div>" % (course))
                    book.write(desc.get_attribute('innerHTML'))
                    book.write("<div><h2>Toc</h2><ul>")
                    for key in dlist.keys():
                        book.write("<li>%s</li>" % (key))
                    book.write("</ul></div>")
                    book.write('</body></html>')

                og = driver.find_element_by_css_selector("meta[property='og:type']")
                if og.get_attribute("content") == "book":
                    doBook(folder, dlist, title)
                else:
                    doVideo(folder, dlist)
        except Exception as error:
            print(error)
            if os.path.exists(folder):
                shutil.rmtree(folder, ignore_errors=True)

def doTopic(topic):
    global driver, topicNum

    n = topicNum
    while True:
        n += 1
        driver.get("%s?page=%s" % (topic, n))

        elements = []
        links = driver.find_elements_by_css_selector("a.t-title")
        if len(links) > 0:
            for link in links:
                # cuteprint(link)
                elements.append(link.get_attribute('href'))
            for element in elements:
                doCourse(element)
        else:
            break

def doBook(folder, dlist, title):
    global driver, pdfReactor

    resFolder = "%s/res" % (folder)
    if not os.path.exists(resFolder):
        os.mkdir(resFolder)

    for css in ["safaribooks.css", "annotator.css", "font-awesome.min.css", "ibis.css"]:
        shutil.copyfile("store/%s" % (css), "%s/%s" % (resFolder, css))

    with open("%s/%s.html" % (folder, title), "w", encoding="utf8") as book:
        book.write('<html> \
<head> \
<meta charset="UTF-8"/> \
<link rel="stylesheet" href="res/safaribooks.css" type="text/css" /> \
<link rel="stylesheet" href="res/annotator.css" type="text/css" /> \
<link rel="stylesheet" href="res/font-awesome.min.css" type="text/css" /> \
<link rel="stylesheet" href="res/ibis.css" type="text/css" /> \
</head> \
<section class="reading sidenav scalefonts subscribe-panel library nav-collapsed"> \
<div id="container" class="application" style="height: auto;"> \
<section role="document"> \
<div id="sbo-rt-content" style="transform: none;"> \
')
        imgN = 0
        prevContent = ""
        for name, url in dlist.items():
            cuteprint(name)

            driver.get(url)

            div = driver.find_element_by_css_selector("div#sbo-rt-content")
            content = div.get_attribute('innerHTML')

            if '<nav epub:type="toc" id="toc">' in content:
                continue

            if content == prevContent:
                continue
            prevContent = content

            for image in div.find_elements_by_css_selector("img"):
                src = image.get_attribute('src')

                fileName, fileExt = os.path.splitext(src)
                imgN += 1
                resImg = "res/%s%s" % (imgN, fileExt)

                with open("%s/%s" % (folder, resImg), 'wb') as merged:
                    res = requests.get(src, stream=True)
                    merged.write(res.raw.data)

                src = src.replace("https://www.safaribooksonline.com", "")
                content = content.replace(src,resImg)

            book.write(content)

        book.write('</div> \
</section> \
</div> \
</body> \
</html>')

        if pdfReactor != None:
            try:
                absFolder = os.path.abspath(folder)
                config = {
                    'document': "file:///%s/%s.html" % (absFolder, title),
                    'baseURL': "file:///%s/" % (absFolder),
                    'logLevel': PDFreactor.LogLevel.WARN,
                    'title': title,
                    'author': "Safari Books Online",
                    'addLinks': True,
                    'addBookmarks': True,
                    'viewerPreferences': [
                        PDFreactor.ViewerPreferences.FIT_WINDOW,
                        PDFreactor.ViewerPreferences.PAGE_MODE_USE_THUMBS
                    ]
                }
                pdf = pdfReactor.convertAsBinary(config)
                if pdf != None:
                    with open("%s/%s.pdf" % (folder, title), "wb") as pdfile:
                        pdfile.write(pdf)
            except Exception as error:
                print(error)

def doVideo(folder, dlist):
    global driver, proxy

    for name, url in dlist.items():
        cuteprint(name)

        proxy.new_har("safaribooks")

        n = 0
        found = False
        while not found:
            n -= 1
            if n < 0:
                n = 12
                driver.get(url)
            time.sleep(5)
            # cuteprint("... loop")
            har = proxy.har
            for entry in har['log']['entries']:
                playlist = entry['request']['url']
                if "index.m3u8" in playlist:
                    res = requests.get(playlist)
                    files = [line.rstrip() for line in res.text.splitlines() if line.rstrip().endswith('.ts')]
                    del res
                    with open("%s/%s.ts" % (folder, name), 'wb') as merged:
                        for file in files:
                            # cuteprint(file)
                            res = requests.get(file, stream=True)
                            merged.write(res.raw.data)
                    found = True


with open("safariscrap.json", "r") as f:
    credentials = json.load(f)

browserMob = ".%sbrowsermob-proxy-2.1.4%sbin%sbrowsermob-proxy" % (os.path.sep, os.path.sep, os.path.sep)
server = Server(browserMob)
server.start()
proxy = server.create_proxy()

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--proxy-server={0}".format(proxy.proxy))
driver = webdriver.Chrome(chrome_options = chrome_options)

# phantom_options = [
#    '--ignore-ssl-errors=true',
#    '--proxy=%s' % (proxy.proxy),
#    '--proxy-type=http'
#    ]
# driver = webdriver.PhantomJS(service_args=phantom_options)

driver.set_window_size(1000, 1000)
driver.get("https://www.safaribooksonline.com/accounts/login")
driver.find_element_by_id('id_email').send_keys(credentials["username"])
driver.find_element_by_id("id_password1").send_keys(credentials["password"])
driver.find_element_by_name("login").click()

for course in courses:
    doCourse(course)

# print(driver.current_url)
server.stop()
driver.quit()