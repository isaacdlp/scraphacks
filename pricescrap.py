# #!/usr/bin/python
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


import re, csv, json
from random import shuffle
import requests as req
from robobrowser import RoboBrowser
from robobrowser.forms.fields import Input
from lxml import etree


prices_file = "pricescrap.csv"

assets = [
    {
        "url": "https://www.bolsasymercados.es/mab/esp/SICAV/Ficha/VALENCIANA_DE_VALORES_S_A___SICAV_ES0182790032.aspx",
        "name": "Valenciana de Valores",
        "id": "ES0182790032"
    },
    {
        "url": "http://tools.morningstar.es/0sgtldtyat/snapshot/snapshot.aspx?SecurityToken=F0GBR052L6]2]0]FOESP$$PEN",
        "name": "Ibercaja Gestión Crecimiento PP",
        "id": "N2602"
    },
    {
        "url": "https://www.quefondos.com/es/planes/ficha/?isin=N2676",
        "name": "Ibercaja Pensiones Bolsa Global",
        "id": 'N2676'
    }
]


def clean_string(str_in):
    str_out = str_in[0].text
    if "." in str_out:
        str_out = re.sub(",", "", str_out)
    str_out = re.sub("\.", "", str_out)
    str_out = re.sub("[^0-9^\/^,]", "", str_out)
    return str_out


# Stateless part

shuffle(assets)

with open(prices_file, "w", newline="") as f:
    csvWriter = csv.writer(f, delimiter=";")
    for index, asset in enumerate(assets):

        try:
            url = asset["url"]
            resp = req.get(url)
            html = etree.HTML(resp.text)

            if "www.bolsasymercados.es" in url:
                asset["date"] = clean_string(html.xpath("//*[@id=\"Contenido_fCab\"]/div[2]/div/div[1]/div[1]/p[1]"))
                asset["value"] = clean_string(html.xpath("//*[@id=\"Contenido_fCab\"]/div[2]/div/div[1]/div[2]/p[1]"))
            elif "tools.morningstar.es" in url:
                asset["date"] = clean_string(html.xpath("//*[@id=\"snapshot_keystatsDefault\"]/div[4]/div[1]/span"))
                asset["value"] = clean_string(html.xpath("//*[@id=\"snapshot_keystatsDefault\"]/div[4]/div[2]"))
            elif "www.quefondos.com" in url:
                asset["date"] = clean_string(html.xpath("//*[@id=\"col3_content\"]/div/div[4]/p[3]/span[2]"))
                asset["value"] = clean_string(html.xpath("//*[@id=\"col3_content\"]/div/div[4]/p[1]/span[2]"))

            csvWriter.writerow([asset["id"], asset["date"], asset["value"]])
            print("%i | %s | %s | %s" % (index + 1, asset["name"], asset["date"], asset["value"]))
        except:
            print(asset)
            print("%i | ERROR processing %s" % (index + 1, asset["name"]))


# Stateful part

with open("duolingoscrap.json", "r") as f:
    credentials = json.load(f)

browser = RoboBrowser(history=True, parser="html.parser", )
browser.open("http://eafi.openfinance.es/login.aspx")
form = browser.get_form(action="./login.aspx")
form.add_field(Input("<input name='__EVENTTARGET' value='ctl00$content$BtAcceptNew'>"))
form["ctl00$content$txtLoginNew"].value = credentials["username"]
form["ctl00$content$txtPasswordNew"].value = credentials["password"]
browser.submit_form(form)

browser.open("http://eafi.openfinance.es/admin/producto/adminProductos.aspx")
form = browser.get_form(action="./adminProductos.aspx")
form.add_field(Input("<input name='__EVENTTARGET' value='ctl00$content$btnCargar'>"))
form['ctl00$content$fuCargarCot'].value = open(prices_file, 'r')
browser.submit_form(form)

form = browser.get_form(action="./adminProductos.aspx")
form.add_field(Input("<input name='__EVENTTARGET' value='ctl00$content$btnAceptarCotizaciones'>"))
browser.submit_form(form)