import requests
from bs4 import BeautifulSoup
import json
import re
import csv
# import mysql.connector
# import configparser
# import plotly
# import plotly.graph_objs as go

### global variables ###
# base url for makeing requests in NPS
baseurl = "https://www.theinfatuation.com"


class Bar:
    def __init__(self, name, rev="", addr="", phone_num='', url='', price='', hours=[], img='', neigh=''):

        self.name = name
        self.addr = addr
        self.review = rev
        self.phone = phone_num
        self.url = url
        self.price = price
        self.hours = hours
        self.neigh = neigh
        self.img = img

    def __str__(self):
        return "{} is located at {} in {}. Its phone number is {}. Its website is {}".format(self.name, self.addr, self.neigh, self.phone, self.url)

    def set_neigh(self, neigh_dict):
        if self.neigh in neigh_dict:
            # update the neighborhood from the name to an ID: set up the foreign key
            self.neigh = neigh_dict[self.neigh]


def get_bars():
    main_url = '/new-york/guides/the-manhattan-bar-directory'
    main_page = BeautifulSoup(
        make_request_using_cache(baseurl, main_url), 'html.parser')
    bars = main_page.findAll('div', class_="spot-block")
    neighls = []
    barls = []

    for bar in bars:
        # the page for next round of scripting, not the bar's url
        bar_rev_url = bar.find('a').get('href')

        ### gather general bar info: name, price rating, address, neighborhood, img ###
        bar_name = bar.find('h3').text.strip()
        bar_price = bar.find(
            'span', class_='address-price-rating')['data-price']

        try:
            bar_img = bar.find('div', class_='spot-block__image-wrapper')
            bar_img = bar_img.find('img').get('src')
        except Exception:
            bar_img = 'No image available.'

        # the single line address
        try:
            bar_addr = bar.find(
                'div', class_='spot-block__address').text
            for t in bar_addr:
                bar_addr = bar_addr.replace('$', '').strip()
        except:
            bar_addr = 'No address available.'
        print(bar_name)

        # find the neighborhood that the bar is located in
        try:
            bar_neigh = bar.find('div', class_='overview-content')
            bar_neigh = bar_neigh.select(
                'a[href^="/new-york/neighborhoods/"]')[0].text
        except:
            bar_neigh = 'No neighborhood identified.'

        # create a list of neighborhoods
        if bar_neigh not in neighls:
            neighls.append(bar_neigh)

        ### scrape the individual page to get additional details: phone, website, open hours, review###
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

        # review contains double quotes and single quotes
        bar_rev = detail_page.find(
            'p' > 'div', class_='post__content__text-block').text

        new_Bar = Bar(name=bar_name, rev=bar_rev, addr=bar_addr, phone_num=bar_phone,
                      url=bar_url, price=bar_price, hours=opens, img=bar_img, neigh=bar_neigh)
        barls.append(new_Bar)

    return (barls, neighls)


def create_bar_csv(barls):
    with open('bars_info.csv', mode='w', newline='') as bars:
        fieldnames = ['name', 'price', 'img', 'web',
                      'addr', 'hours', 'review', 'neighborhood']
        bar_writer = csv.DictWriter(bars, fieldnames=fieldnames)

        bar_writer.writeheader()

        for bar in barls:
            bar_writer.writerow({'name': bar.name, 'price': bar.price, 'img': bar.img, 'web': bar.url,
                                 'addr': bar.addr, 'hours': bar.hours, 'review': bar.review, 'neighborhood': bar.neigh})


def create_neigh_csv(neigh_dict):
    with open('neighborhoods.csv', mode='w', newline='') as bars:
        fieldnames = ['id', 'name']
        writer = csv.DictWriter(bars, fieldnames=fieldnames)

        writer.writeheader()

        for name, i in neigh_dict.items():
            writer.writerow({'name': name, 'id': i})


def get_neigh(neighls):
    neigh_dict = {}
    for i in range(len(neighls)):
        neigh_dict[neighls[i]] = i+1
    return neigh_dict


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


(barls, neighls) = get_bars()
neigh_dic = get_neigh(neighls)
for bar in barls:
    bar.set_neigh(neigh_dic)  # update the foreign key

create_bar_csv(barls)
create_neigh_csv(neigh_dic)
