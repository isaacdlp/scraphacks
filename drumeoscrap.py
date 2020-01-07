#!/usr/bin/python
# -*- coding: utf-8 -*-


# ScrapHacks
# Web Scrapping Examples
#
# Copyright 2017-2018 Isaac de la Pena <isaacdlp@agoraeafi.com>
#
# Licensed under the MIT License (the "License")
# you may not use this file except in compliance with the License.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from selenium import webdriver
from bs4 import BeautifulSoup as soup
from browsermobproxy import Server
from time import sleep
from functools import partial
import requests as req
import subprocess as sub
import os, shutil, json, unicodedata


# Generic Functions


normalize = partial(unicodedata.normalize, 'NFC')

def cleanName(name):
    max = 100
    pre = "".join([c for c in name if c.isalpha() or c.isdigit() or c == ' ']).strip(' ').replace('  ',' ')
    if len(pre) > max:
        pre = pre[0:max]
    return pre

def doList(listFile, listFolder, blackFile, stages=None):
    series = []
    with open(listFile, "r") as fin:
        htmlFile = fin.read()
    html = soup(htmlFile, "html.parser")

    for dir in os.walk(listFolder):
        existing = list(map(normalize, dir[1]))
        break

    with open(blackFile, "r") as fin:
        blacklist = list(map(normalize, json.load(fin)))

    for serie in html.select("a.flex-row"):
        link = serie.get("href")
        if not link:
            continue
        level = cleanName(serie.select_one("div.x-tiny").text)
        if stages:
            for n, stage in enumerate(stages, start=1):
                if stage == level:
                    level = "%02d" % n
                    break
        else:
            level = level.split(" ")[1]
            if len(level) == 1:
                level = "0%s" % level
        title = cleanName(serie.select_one("p.item-title").text)
        if stages:
            band = cleanName(serie.select_one("p.text-drumeo").text)
            title = "%s - %s" % (band, title)
        name = "%s %s" % (level, title)

        name = normalize(name)
        if name in existing:
            existing.remove(name)
        elif name in blacklist:
            blacklist.remove(name)
        else:
            series.append((link, name))

    if len(existing) > 0 or len(blacklist) > 0:
        raise Exception("There are unmatched series %s %s" % (existing, blacklist))

    series.sort(key = lambda x: x[1])
    return series

def doPart(partLink, partName, seriesName, seriesFolder, index=0):
    minLesson = 0
    if minLesson > 0 and index < minLesson:
        return

    videoName = "%s.mp4" % partName
    if index > 0:
        videoName = "%02d %s" % (index, videoName)

    driver.get(partLink)
    sleep(5)

    # Download additional resources
    if index < 2:
        resources = ["pdf", "zip"]
        materials = None
        try:
            materials = driver.find_element_by_css_selector("div.download-dropdown")
        except:
            print("No course resources")
        if materials:
            for material in reversed(materials.find_elements_by_css_selector("a")):
                href = material.get_attribute("href")
                for resource in resources:
                    if href.lower().endswith(resource):
                        print("Downloading %s" % resource)
                        res = req.get("%s" % href)
                        if res.status_code != 200:
                            raise Exception("File %s did not download properly" % href)
                        with open("%s/%s.%s" % (seriesFolder, seriesName[3:], resource), 'wb') as bout:
                            bout.write(res.content)
                        resources.remove(resource)
                        break

    print("%02d %s" % (index, partName))

    # Change the quality
    isNewPlayer = True
    try:
        driver.execute_script("document.querySelector('div.settings-drawer').style.display = 'block';")
        driver.execute_script("document.querySelector('div.settings-drawer div.flex-row:nth-of-type(2)').style.display = 'block';")
    except:
        isNewPlayer = False
        try:
            driver.execute_script("document.querySelector('div.mejs__qualities-selector').classList.remove('mejs__offscreen');")
        except:
            raise Exception("Unrecognized player... Embedded YouTube?")

    qualityEl = "input.mejs__qualities-selector-input"
    if isNewPlayer:
        qualityEl = "div.settings-drawer ul:nth-of-type(1) li"

    sleep(5)
    qualityIndex = None
    for qualityTarget in qualityTargets:
        for n, qualities in enumerate(driver.find_elements_by_css_selector(qualityEl)):
            quality = qualities.text
            if not isNewPlayer:
                quality = qualities.get_attribute("value")
            pos = cleanName(quality).find(qualityTarget)
            if pos >= 0:
                qualityIndex = n
                break
        if qualityIndex is not None:
            break
    if qualityIndex is None:
        raise Exception("Could not find any of the target qualities %s!" % qualityTargets)

    #driver.find_elements_by_css_selector(qualityEl)[quality].click()
    driver.execute_script("document.querySelectorAll('%s')[%s].click();" % (qualityEl, qualityIndex))
    sleep(5)

    # Start the video
    proxy.new_har("drumeo")

    videoWrap = driver.find_element_by_id("lessonVideoWrap")
    videoWrap.click()

    # Capture the video root
    timer = 0
    videoWeb = None
    while not videoWeb:
        timer += 1
        if timer > 30:
            break
        sleep(2)
        har = proxy.har
        for entry in har['log']['entries']:
            videoUrl = entry['request']['url']
            if isNewPlayer:
                pos = videoUrl.find("segment-")
                if pos >= 0:
                    videoWeb = videoUrl[:(pos+8)]
                    break
            else:
                if videoUrl.endswith(".mp4"):
                    videoWeb = videoUrl
                    break

    if not videoWeb:
        raise Exception("Video root not found")

    # Stop the video
    videoWrap.click()
    #action = webdriver.common.action_chains.ActionChains(driver)
    #action.move_to_element_with_offset(videoWrap, 100, 100)
    #action.click()
    #action.perform()

    if isNewPlayer:
        # Download the segments
        videoFolder = "%s/_tmp" % seriesFolder
        if not os.path.exists(videoFolder):
            os.makedirs(videoFolder)

        x = 1
        segments = []
        while True:
            res = req.get("%s%s.ts" % (videoWeb, x))
            if res.status_code != 200:
                break
            segmentFile = "%s/segment-%s.ts" % (videoFolder, x)
            with open(segmentFile, 'wb') as bout:
                bout.write(res.content)
            segments.append("file '%s'" % segmentFile)
            x += 1

        with open("%s/segments.txt" % videoFolder, "w") as fout:
            fout.write("\n".join(segments))

        # Concatenate with FFMPEG
        cvf = videoFolder.replace(" ", "\ ")
        sub.call("%s -f concat -i %s/segments.txt -c copy %s/segments.ts" % (ffmpegExe, cvf, cvf),
                 shell=True, stderr=sub.DEVNULL, stdout=sub.DEVNULL)
        sub.call("%s -i %s/segments.ts -strict -2 -vcodec copy %s/segments.mp4" % (ffmpegExe, cvf, cvf),
                 shell=True, stderr=sub.DEVNULL, stdout=sub.DEVNULL)
        # Rename and clean
        shutil.move("%s/segments.mp4" % (videoFolder), "%s/%s" % (seriesFolder, videoName))
        shutil.rmtree("%s" % videoFolder, ignore_errors=True)
    else:
        res = req.get("%s" % videoWeb)
        if res.status_code != 200:
            raise Exception("Video did not download from %s" % videoWeb)
        with open("%s/%s" % (seriesFolder, videoName), 'wb') as bout:
            bout.write(res.content)


# Generic Parameters


# https://www.drumeo.com/trial
loginWeb = "https://www.drumeo.com/login/?lf=0"
coursesWeb = "https://www.drumeo.com/members/lessons/courses"
songsWeb = "https://www.drumeo.com/members/lessons/songs"

cookiesFile = "./drumeoscrap.cookie"
credsFile = "./drumeoscrap.json"
coursesFile = "./drumeo_courses.html"
noCoursesFile = "./drumeo_courses.black"
songsFile = "./drumeo_songs.html"
noSongsFile = "./drumeo_songs.black"
coursesFolder = "/Volumes/SAMSUNG/Music/Drums/Drumeo/Lessons"
songsFolder = "/Volumes/SAMSUNG/Music/Drums/Drumeo/Songs"

levelsList = ["all", "beginner", "intermediate", "advanced"]
ffmpegExe = "/Users/isaacdlp/Downloads/Tools/FFMPEG/ffmpeg"
qualityTargets = ["360", "270", "540"]


# Specific Functionality


# Set up lists
courses = doList(coursesFile, coursesFolder, noCoursesFile)
songs = doList(songsFile, songsFolder, noSongsFile, levelsList)
print("- - -")
print("%s courses to download" % len(courses))
print("%s songs to download" % len(songs))
if (len(courses) + len(songs) == 0):
    exit(0)

try:

    # Set up browser
    browserMob = ".%sbrowsermob-proxy-2.1.4%sbin%sbrowsermob-proxy" % (os.path.sep, os.path.sep, os.path.sep)
    server = Server(browserMob)
    server.start()
    proxy = server.create_proxy()

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--proxy-server={0}".format(proxy.proxy))
    driver = webdriver.Chrome(chrome_options = chrome_options)

    driver.set_window_size(1000, 1000)

    # Read cookies
    cookies = None
    try:
        with open(cookiesFile, "r") as fin:
            cookies = json.load(fin)

        for site in ["drumeo.com"]:
            driver.get("https://%s" % site)
            for cookie in cookies:
                if site in cookie["domain"]:
                    driver.add_cookie(cookie)
    except:
        print("No cookies found")

    driver.get(coursesWeb)

    # Login if needeed
    isLogin = None
    try:
        isLogin = driver.find_element_by_id('loginEmail')
    except:
        pass
    if isLogin:
        print("Logging in...")

        with open(credsFile, "r") as fin:
            credentials = json.load(fin)

        driver.find_element_by_id('loginEmail').send_keys(credentials["username"])
        driver.find_element_by_id("loginPassword").send_keys(credentials["password"])
        driver.find_element_by_css_selector("#loginForm > form > button").click()

    # Write cookies
    cookies = driver.get_cookies()
    with open(cookiesFile, "w") as fin:
        json.dump(cookies, fin, indent=2)

    # Get courses
    for courseLink, courseName in courses:
        print("- - -")
        print("Processing '%s'" % courseName)

        folderCourse = "%s/_%s" % (coursesFolder, courseName)
        if not os.path.exists(folderCourse):
            os.makedirs(folderCourse)

        driver.get(courseLink)

        lessons = []
        web = driver.find_element_by_css_selector("div[card_type='list']")
        for lesson in web.find_elements_by_css_selector("a.flex-row"):
            link = lesson.get_attribute("href")
            name = cleanName(lesson.find_element_by_css_selector("p.item-title").text)
            lessons.append((link, name))

        # Get lessons
        for index, (lessonLink, lessonName) in enumerate(lessons, start=1):

            doPart(lessonLink, lessonName, courseName, folderCourse, index)

        shutil.move(folderCourse, "%s/%s" % (coursesFolder, courseName))

    # Get songs
    for songLink, songName in songs:
        print("- - -")
        print("Processing '%s'" % songName)

        folderSong = "%s/_%s" % (songsFolder, songName)
        if not os.path.exists(folderSong):
            os.makedirs(folderSong)

        doPart(songLink, songName[3:], songName, folderSong)

        shutil.move(folderSong, "%s/%s" % (songsFolder, songName))

finally:
    server.stop()
    driver.quit()