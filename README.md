# Scrap Hacks
Useful Web Scrapping "Hacks"

## Duolingo

Use `duolingoscrap.py` to complile *cheat sheets* from [Duolingo](https://www.duolingo.com).

It portrays the use of [Selenium](http://www.seleniumhq.org) and [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/).

### Installation

* Install the [Chrome Browser](https://www.google.com/chrome)
* Install [Python 3](https://www.python.org)
* Install **BeautifulSoup**
`pip install bs4`
* Install **Selenium**
`pip install selenium`
* Add to your system the required [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads)
* Edit your duolingo credentials in `duolingoscrap.json` (see "General Requirements" below).

### Usage

* Duplicate the template `duolingo/duo.html` with the name of the language you want to download (e.g. `duolingo/Russian.html`).
* Optionally you can edit the parts that correspond to the name of the language and the flag:

```
<div class="_1sdh6 ljpAk">
    <div class="yZINH">
        <!-- This section has the flag -->
        <span class="_1eqxJ _3viv6 HCWXf _3PU7E _2XSZu"></span>
    </div>
    <div class="yZINH _1_vhy">
        <!-- This section has the name -->
        <h2>Russian</h2>
        <div><span>Cheat Sheet</span></div>
    </div>
</div>
```

* Edit the `languages` dictionary inside `duolingoscrap.py` to associate Duolingo's extension for the language (e.g. `ru`) to your recently created file (e.g. `duolingo/Russian.html`).

```
languages = {
    "ru": "duolingo/Russian.html"
}
```

* You have two options: download only selected lessons (add them to the `lessons` array), or the whole language (leave the `lessons` array empty). In the second case note that:
** It will only scan the active language. If you have several languages in Duolingo, you need to switch to the language that you want to download.
** It will only download up to your last available lesson. It can't download lessons you can't access yet (but you can run the program again on a future date).
** It keeps track of the lessons you already downloaded and will **not** overwrite or duplicate them.

* Run the program
`python duolingoscrap.py`

## Safari Books

Use `safariscrap.py` to download *books* and *video lessons* from [SafariBooks](https://www.safaribooksonline.com/).

It combines **Selenium** with [Browsermobproxy](https://github.com/lightbody/browsermob-proxy) to observe and manipulate web traffic (required in for video download) and [PdfReactor](http://www.pdfreactor.com/) to convert HTML books into PDF.

### Installation

* Follow all the instructions above (credentials in `safariscrap.json`)
* Install [Java](https://www.java.com/en) (Required by BrowserMobProxy)
* Optionally, install [PdfReactor](http://www.pdfreactor.com/).
** If you use PdfReactor switch the `pdfReactor` variable in `safariscrap.py` accordingly:

```
pdfReactor = None
# pdfReactor = PDFreactor("http://localhost:9423/service/rest")
```

### Usage

* Search in [SafariBooks](https://www.safaribooksonline.com) what you want to download. You have two options:
** Download a specific course like `https://www.safaribooksonline.com/library/view/numpy-cookbook/9781849518925/`.
*** The application will automatically detect whether it is a **book** or a **video tutorial** and proceed accordingly.
** Download **ALL** courses from a given topic like `https://www.safaribooksonline.com/topics/python`
* List any combination of topics and courses in any order in the `courses` array.

```
courses = [
    "https://www.safaribooksonline.com/library/view/python-data-structures/9781786467355/",
    "https://www.safaribooksonline.com/topics/java"
]

```

** Useful Notes for topics with many courses:
*** If you just list one topic, you can further refine the **page** it starts downloading from using the `topicNum` variable.
*** By default the program will **NOT** overwrite courses downloaded previously. You can switch this with the `overwrite` variable.

```
overwrite = False
topicNum = 0
```

* Run the program
`python safariscrap.py`

## General Requirements

In both cases you need to create a credentials file named `duolingoscrap.json` or `safariscrap.json` with the following structure:

```
{
  "username" : "<your_username>",
  "password" : "<your_password>"
}
```
