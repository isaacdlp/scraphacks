from scrapper import *
import requests as req

target = "isaacdlp"

folder = "download/%s" % target
if not os.path.exists(folder):
    os.mkdir(folder)

scrapper = Scrapper()
try:
    scrapper.start()
    scrapper.login("instagram")
    props = scrapper.instagram("https://www.instagram.com/%s" % target)
finally:
    scrapper.stop()

for i, prop in enumerate(props["Media"], start = 1):
    res = req.get(prop["src"])
    if res.status_code != 200:
        break
    with open("%s/%s-%s.%s" % (folder, target, i, prop["type"]), 'wb') as bout:
        bout.write(res.content)