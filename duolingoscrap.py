#!/usr/bin/python
# -*- coding: utf-8 -*-


# ScrapHacks
# Web Scrapping Examples
#
# Copyright 2017-2018 Isaac de la Pena <isaacdlp@agoraeafi.com>
#
# Licensed under the MIT License (the "License");
# you may not use this file except in compliance with the License.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup as soup
import json
import sys


languages = {
    "pt": "duolingo/Portuguese.html",
    "ru": "duolingo/Russian.html",
    "es": "duolingo/Spanish.html",
    "tr": "duolingo/Turkish.html",
    "ca": "duolingo/Catalan.html",
    "en": "duolingo/English.html",
    "it": "duolingo/Italian.html",
    "fr": "duolingo/French.html",
}

caches = { }

lessons = [
    #"https://www.duolingo.com/skill/pt/Basics-1",
    #"https://www.duolingo.com/skill/pt/Basics-2",
    #"https://www.duolingo.com/skill/ru/Where-is-it%3F",
    #"https://www.duolingo.com/skill/ru/Animals-1",
    #"https://www.duolingo.com/skill/ru/Genitive-Case---1",
    #"https://www.duolingo.com/skill/ru/Possessive-Modifiers-1",
    #"https://www.duolingo.com/skill/pt/Travel",
    #"https://www.duolingo.com/skill/pt/Directions",
    #"https://www.duolingo.com/skill/pt/Feelings",
    #"https://www.duolingo.com/skill/pt/Verbs%3A-Present-Perfect",
    #"https://www.duolingo.com/skill/pt/Sports",
    #"https://www.duolingo.com/skill/pt/Abstract-Objects-1",
    #"https://www.duolingo.com/skill/pt/Verbs%3A-Past-Perfect"
]


def cuteprint(text):
    print(text.encode(sys.stdout.encoding, 'ignore'))

def doLesson(lesson):
    global driver, languages, caches

    cuteprint(lesson)

    i1 = lesson.rfind("/")
    anchor = lesson[(i1 + 1):]
    i2 = lesson.rfind("/", 0, i1)
    lang = lesson[(i2 + 1):i1]
    file_name = languages[lang]

    if lang in caches:
        file_html = caches[lang]
    else:
        with open(file_name, "r") as f:
            file_html = soup(f.read(), "html.parser")
            caches[lang] = file_html

    duo_base = file_html.select("div#duo_base")[0]
    duo_toc = file_html.select("div#duo_base > ol")[0]

    priors = duo_toc.select("a[href='#%s']" % anchor)
    if len(priors) == 0:
        driver.get(lesson)
        sleep(10)

        anchor_tag = soup("<a name='%s'></a>" % anchor, "html.parser")
        duo_base.append(anchor_tag)

        title = driver.find_element_by_css_selector("div._1_vhy h2").text
        try:
            section = driver.find_element_by_css_selector("div._33Zau")
            section_html = soup(section.get_attribute("outerHTML"), "html.parser")
        except:
            cuteprint("Apparently it is EMPTY!")
            section_html = soup("<div class=\"_33Zau\"><hr><h2>Empty</h2></div>", "html.parser")

        section_html.find("h2").string.replace_with(title)
        duo_base.append(section_html)

        link_tag = soup("<li><a href='#%s'>%s</a></li>" % (anchor, title), "html.parser")
        duo_toc.append(link_tag)

        caches[lang] = soup(str(file_html), "html.parser")
    else:
        cuteprint("Anchor #%s already exists!" % anchor)


with open("duolingoscrap.json", "r") as f:
    credentials = json.load(f)

driver = webdriver.Chrome()

try:
    driver.set_window_size(1000, 1000)
    driver.get("https://www.duolingo.com")
    driver.find_element_by_id("sign-in-btn").click()
    driver.find_element_by_id("top_login").send_keys(credentials["username"])
    driver.find_element_by_id("top_password").send_keys(credentials["password"])
    driver.find_element_by_id("login-button").click()

    sleep(10)

    if len(lessons) == 0:
        els = driver.find_elements_by_css_selector("div.i12-l a.W1dac")
        for el in els:
            lessons.append(str(el.get_attribute("href")))

    for lesson in lessons:
        doLesson(lesson)

    for lang in caches.keys():
        file_html = caches[lang]
        file_name = languages[lang]
        with open(file_name, "wb") as f:
            f.write(file_html.prettify(encoding="utf-8"))

except Exception as e:
    cuteprint("ERROR: %s" % str(e))

driver.quit()
