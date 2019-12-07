import requests
from bs4 import BeautifulSoup
import json
# import plotly
# import plotly.graph_objs as go

### global variables ###
# base url for makeing requests in NPS
baseurl = "https://www.theinfatuation.com"


class Bar:
    def __init__(self, name, desc="", address=[""], phone_num='', url='', price='', hours=[]):

        self.name = name
        self.address = address
        self.desc = desc
        self.phone = phone_num
        self.url = url
        self.price = price
        self.hours = hours

        try:
            self.description = desc
            self.address = "{}, {},{} {}".format(
                address_all[0], address_all[1], address_all[2], address_all[3]
            )
        except:
            self.description = "No description found"
            self.address = "No address found"

    def __str__(self):
        return "{} is located at {}. Its phone number is {}. Its website is at {}".format(self.name, self.address, self.phone, self.url)


def get_bars():
    main_url = '/new-york/guides/the-manhattan-bar-directory'
    main_page = BeautifulSoup(
        make_request_using_cache(baseurl, main_url), 'html.parser')
    bars = main_page.findAll('div', class_="spot-block")

    for bar in bars[:10]:
        bar_name = bar.find('h3').text.strip()
        # the page for next round of scripting, not the bar's url
        bar_rev_url = bar.find('a').get('href')
        bar_price = bar.find(
            'span', class_='address-price-rating')['data-price']
        # the single line address
        bar_addr = bar.find(
            'div', class_='spot-block__address').text
        for t in bar_addr:
            bar_addr = bar_addr.replace('$', '').strip()

        # find the neighborhood that the bar is located in

        bar_neigh = bar.find('div', class_='overview-content')
        print(bar_neigh)

        try:
            bar_img = bar.find('div', class_='spot-block__image-wrapper')
            bar_img = bar_img.find('img').get('src')
        except Exception:
            bar_img = 'No image available.'

        # scrape the individual page to get additional details
        html = make_request_using_cache(baseurl, bar_rev_url)

        detail_page = BeautifulSoup(html, 'html.parser')

        try:
            bar_phone = detail_page.find(
                'a', class_="post__sidebar__info__phone").text
        except Exception:
            bar_phone = 'No phone number available.'

        try:
            bar_url = detail_page.find(class_='post__sidebar__info__website')
            bar_url = bar_url.find('a').get('href')
        except Exception:
            bar_url = 'No website available.'

        bar_hours = detail_page.findAll('div', class_='weekday')
        opens = []
        # hours could be an empty list
        for open_day in bar_hours:
            day = open_day.find('p', class_='weekday__day').text
            hours = open_day.find('p', class_='weekday__hours').text
            open_hours = (day, hours)
            opens.append(open_hours)
        # print(opens)


def params_unique_combination(baseurl, endurl=""):
    fullurl = baseurl + endurl
    return fullurl


# on startup, try to load the cache from file
CACHE_FNAME = "BARS.json"
try:
    cache_file = open(CACHE_FNAME, "r")
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()

# if there was no file, no worries. There will be soon!
except:
    CACHE_DICTION = {}

# The main cache function


def make_request_using_cache(baseurl, endurl=""):
    unique_ident = params_unique_combination(baseurl, endurl)

    # first, look in the cache to see if we already have this data
    if unique_ident in CACHE_DICTION:
        print("Getting cached data...")
        return CACHE_DICTION[unique_ident]

    # if not, fetch the data afresh, add it to the cache,
    # then write the cache to file
    else:
        print("Making a request for new data...")
        resp = requests.get(baseurl + endurl)
        # Load the data from request
        CACHE_DICTION[unique_ident] = resp.text

    # Save the data from request
        dumped_json_cache = json.dumps(
            CACHE_DICTION, indent=4, ensure_ascii=False,)
        fw = open(CACHE_FNAME, "w")
        fw.write(dumped_json_cache)
        fw.close()  # Close the open file
        return CACHE_DICTION[unique_ident]


get_bars()
