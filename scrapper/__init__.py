import json, sys, math, threading, os, re
from random import randrange as rnd
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from playsound import *
from PIL import Image
from io import BytesIO

# Generic objects

class Scrapper():

    def __init__(self, driver = "chrome"):
        self.use_cookies = True
        self.close_on_exit = True
        self.interactive = True
        self.default_cmd = None
        self.audible = False
        self.max_loop = 2
        self.down_timeout = 300
        self.browser = None
        self.own_dir = __path__[0]
        self.down_dir = os.path.abspath("../download")

    def start(self, driver="firefox"):
        if not self.browser:
            if driver == "firefox":
                options = webdriver.FirefoxOptions()
                options.set_preference("dom.push.enabled", False)
                options.set_preference("browser.download.folderList", 2)
                options.set_preference("browser.download.manager.showWhenStarting", False)
                options.set_preference("browser.download.dir", self.down_dir)
                options.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv, application/pdf")
                self.browser = webdriver.Firefox(executable_path="%s/geckodriver" % self.own_dir,
                                                 log_path="%s/geckodriver.log" % self.own_dir, firefox_options=options)
            elif driver == "chrome":
                chrome_options = webdriver.ChromeOptions()
                options = {
                    "profile.default_content_setting_values.notifications": 2,
                    "download.default_directory": self.down_dir,
                    "download.prompt_for_download": False,
                    "download.directory_upgrade": True,
                    "plugins.always_open_pdf_externally": True
                }
                chrome_options.add_experimental_option("prefs", options)
                self.browser = webdriver.Chrome("%s/chromedriver" % self.own_dir, chrome_options=chrome_options)
            elif driver == "safari":
                self.browser = webdriver.Safari()

            if self.browser:
                self.browser.set_window_size(1200, 1000)

        return self.browser

    def wait(self, val1=0, val2=0):
        if val1 == 0:
            val1 = 1
            val2 = 5
        if val2 == 0:
            sleep(val1)
        else:
            sleep(rnd(val1, val2))

    def _play(self, props):
        while props["loop"] < self.max_loop:
            playsound("%s/chime.mp3" % __path__)
            props["loop"] += 1

    def _proxy(self, fun, var = None):
        if self.browser:
            successful = False
            while not successful:
                try:
                    return fun(var)
                except Exception as e:
                    if self.interactive:
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        print("ERROR '%s' at line %s" % (e, exc_tb.tb_lineno))

                        cmd = self.default_cmd
                        if not cmd:
                            props = {"loop": 0}
                            if self.audible:
                                thread = threading.Thread(target=self._play, args=(props,))
                                thread.start()
                            cmd = input("*(r)epeat, (c)ontinue, (a)bort or provide new url? ")
                            props["loop"] = self.max_loop
                        if cmd == "r" or cmd == "":
                            pass
                        elif cmd == "c":
                            successful = True
                        elif cmd == "a":
                            raise e
                        else:
                            var = cmd
                    else:
                        raise e

    def _print(self, text):
        if self.interactive:
            print(text)

    def _base(self, url):
        props = {}

        url = url.strip()

        if url != self.browser.current_url:
            self.browser.get(url)
            self.wait()

        html = self.browser.find_element_by_css_selector("html")
        lang = html.get_attribute("lang")
        if lang == "en":
            props["Decimal"] = "."
        elif lang == "es":
            props["Decimal"] = ","
        else:
            raise Exception("Unsupported language '%s'" % lang)

        props["Language"] = lang

        return props

    def login(self, site):
        return self._proxy(self._login, site)

    def _cookies(self, site):
        if self.use_cookies:
            try:
                with open("%sscrap.cookie" % site, "r") as f:
                    cookies = json.load(f)

                self.browser.get("https://%s.com" % site)
                for cookie in cookies:
                    if site in cookie["domain"]:
                        self.browser.add_cookie(cookie)

                self.browser.get("https://%s.com" % site)

                self._print("Login with cookies to %s" % site)
                return True
            except:
                pass
        return False

    def _login(self, site):
        with open("%sscrap.json" % site, "r") as f:
            creds = json.load(f)

        if site == "facebook":
            if not self._cookies(site):
                self._print("Login to facebook")
                self.browser.get("https://www.facebook.com/login")
                self.wait()

                login_form = self.browser.find_element_by_css_selector("form#login_form")

                login_email = login_form.find_element_by_name("email")
                login_email.send_keys(creds["username"])

                login_pass = login_form.find_element_by_name("pass")
                login_pass.send_keys(creds["password"])

                login_pass.send_keys(Keys.ENTER)

            self.wait(  )
            self.browser.find_element_by_css_selector("div[data-click='profile_icon']")

        elif site == "instagram":
            if not self._cookies(site):
                self._print("Login to instagram")
                self.browser.get("https://www.instagram.com")
                self.wait()

                login_form = self.browser.find_element_by_css_selector("article form")

                login_email = login_form.find_element_by_name("username")
                login_email.send_keys(creds["username"])

                login_pass = login_form.find_element_by_name("password")
                login_pass.send_keys(creds["password"])

                login_pass.send_keys(Keys.ENTER)

            self.wait(5)
            self.browser.find_element_by_css_selector("nav a[href='/%s/']" % creds["username"])

        if self.use_cookies:
            cookies = self.browser.get_cookies()
            with open("%sscrap.cookie" % site, "w") as f:
                json.dump(cookies, f, indent=2)

        return True

    def screenshot(self, url):
        return self._proxy(self._screenshot, url)

    def _screenshot(self, url):
        url = url.strip()

        if url != self.browser.current_url:
            self.browser.get(url)
            self.wait()

        bytes = None
        try:
            self.browser.execute_script("document.body.style.setProperty('height','auto','important');for(var x=document.body.getElementsByTagName('*'),y=x.length,v=!0,z=0;z<y;z++){var w=window.getComputedStyle(x[z],null);'fixed'==w.getPropertyValue('background-attachment')&&x[z].style.setProperty('background-attachment','scroll','important'),!v||'fixed'!=w.getPropertyValue('position')&&'sticky'!=w.getPropertyValue('position')||(x[z].style.setProperty('position','relative','important'),v=!1)}")
            height_view = self.browser.execute_script("return window.innerHeight;")
            height_total = self.browser.execute_script("return document.body.scrollHeight;")

            height_parts = int(math.ceil(height_total / height_view))
            if height_parts > 15:
                height_parts = 15

            for height_part in range(height_parts, -1, -1):
                self.browser.execute_script("window.scrollTo(0, %s);" % (height_view * height_part))
                self.wait(1)

            ele = self.browser.find_element_by_css_selector("body")
            bytes = BytesIO(ele.screenshot_as_png)
        except:
            pass

        if not bytes:
            bytes = BytesIO(self.browser.get_screenshot_as_png())

        image = Image.open(bytes)
        image = image.convert("RGB")
        buffer = BytesIO()
        image.save(buffer, format="JPEG")

        return buffer.getvalue()

    def scrap_linkedin(self, url):
        return self._proxy(self._linkedin, url)

    def facebook(self, url):
        return self._proxy(self._facebook, url)

    def _facebook(self, url):
        props = self._base(url)

        # Facebook Followers
        elements = self.browser.find_elements_by_css_selector("div#PagesProfileHomeSecondaryColumnPagelet div._6590 div._4bl9")
        for element in elements:
            text = element.text
            if text.endswith("people follow this") or text.endswith("personas siguen esto"):
                props["Facebook Followers"] = text
                break

        if "Facebook Followers" not in props:
            raise Exception("Facebook Followers not Found")

        return props

    def instagram(self, url):
        return self._proxy(self._instagram, url)

    def _instagram(self, url):
        props = self._base(url)

        media = []

        try:
            self.browser.execute_script("document.querySelector('article a').click()")

            while True:
                self.wait()

                try:
                    image = self.browser.find_element_by_css_selector("article.M9sTE img[decoding='auto']")
                    srcset = image.get_attribute("srcset")
                    srcs = [src.split(" ") for src in srcset.split(",")]
                    srcs.sort(reverse=True, key=lambda x: int(x[1][:-1]))
                    src = srcs[0][0]
                    media.append({"type" : "jpg", "src" : src})
                except:
                    try :
                        video = self.browser.find_element_by_css_selector("article.M9sTE video")
                        src = video.get_attribute("src")
                        media.append({"type": "mpg", "src": src})
                    except:
                        pass

                try:
                    self.browser.execute_script("document.querySelector('a.coreSpriteRightPaginationArrow').click()")
                except:
                    break
        except:
            pass

        props["Media"] = media

        return props

    def scroll_down(self, complete = True):
        # Get scroll height.
        last_height = self.browser.execute_script("return document.body.scrollHeight")
        while True:
            # Scroll down to the bottom.
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait to load the page.
            self.wait()
            # Calculate new scroll height and compare with last scroll height.
            new_height = self.browser.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                return complete
            last_height = new_height
            if not complete:
                return True

    def stop(self):
        if self.browser and self.close_on_exit:
            self.browser.quit()