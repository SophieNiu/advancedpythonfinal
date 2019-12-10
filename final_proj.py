import requests
from bs4 import BeautifulSoup
import json
import re
import csv
import sqlite3

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

        ### gather general bar info: name, price rating, address, neighborhood, img,review ###
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
        # print(bar_name)

        # find the neighborhood that the bar is located in
        try:
            bar_neigh = bar.find('div', class_='overview-content')
            bar_neigh = bar_neigh.select(
                'a[href^="/new-york/neighborhoods/"]')[0].text
        except:
            bar_neigh = 'No neighborhood identified.'

        # review contains double quotes and single quotes
        try:
            bar_rev = bar.find(
                'p' > 'div', class_='spot-block__description-section').text.strip()
        except:
            bar_rev = 'No review available'

        # create a list of neighborhoods
        if bar_neigh not in neighls:
            neighls.append(bar_neigh)

        ### scrape the individual page to get additional details: phone, website, open hours###
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
        try:
            for open_day in bar_hours:
                day = open_day.find('p', class_='weekday__day').text
                hours = open_day.find('p', class_='weekday__hours').text
                open_hours = (day, hours)
                opens.append(open_hours)
        except:
            opens = []

        new_Bar = Bar(name=bar_name, rev=bar_rev, addr=bar_addr, phone_num=bar_phone,
                      url=bar_url, price=bar_price, hours=opens, img=bar_img, neigh=bar_neigh)
        barls.append(new_Bar)

    return (barls, neighls)


def create_bar_csv(barls):
    with open('data/bars_info.csv', mode='w', newline='') as bars:
        fieldnames = ['name', 'price', 'img', 'web', 'phone',
                      'addr', 'hours', 'review', 'neighborhood']
        bar_writer = csv.DictWriter(bars, fieldnames=fieldnames)

        bar_writer.writeheader()

        for bar in barls:
            bar_writer.writerow({'name': bar.name, 'price': bar.price, 'img': bar.img, 'web': bar.url,
                                 'phone': bar.phone, 'addr': bar.addr, 'hours': bar.hours, 'review': bar.review, 'neighborhood': bar.neigh})


def create_neigh_csv(neigh_dict):
    with open('data/neighborhoods.csv', mode='w', newline='') as bars:
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
        # print("Getting cached data...")
        return CACHE_DICTION[unique_ident]

    # if not, fetch the data afresh, add it to the cache,
    # then write the cache to file
    else:
        # print("Making a request for new data...")
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


### create table and set up database ###

# Part 1: Read data from CSV and JSON into a new database called nycbars.db
DBNAME = 'nycbars.db'
BARSCSV = 'data/bars_info.csv'
NEIGHBORCSV = 'data/neighborhoods.csv'


def read_csv_to_db(csvfile, header):
    fn = open(csvfile)
    file_data = csv.reader(fn)
    csv_data = []
    for row in file_data:
        if row[0] != header:
            csv_data.append(row)
    return csv_data


def init_db():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    # Drop tables
    statement = '''
        DROP TABLE IF EXISTS 'Bars';
    '''
    cur.execute(statement)
    statement = '''
        DROP TABLE IF EXISTS 'Neighborhoods';
    '''
    cur.execute(statement)

    conn.commit()

    statement = '''
            CREATE TABLE "Neighborhoods" (
            "Id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            "NeighName"	TEXT
            );

            '''
    cur.execute(statement)
    # print('create Neighborhoods table')

    statement = '''
        CREATE TABLE "Bars" (
	    "Id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	    "Name"	TEXT,
	    "Price"	INTEGER,
	    "Image"	TEXT,
	    "Website"	TEXT,
        "Phone"     TEXT,
	    "Address"	TEXT,
	    "Hours"	TEXT,
	    "Review"	TEXT,
	    "Neighborhood"	INTEGER NOT NULL,
        FOREIGN KEY (Neighborhood) REFERENCES Neighborhoods(Id)
    	);

        '''
    cur.execute(statement)
    # print('create Bars table')

    conn.commit()
    conn.close()


def insert_data(bar_db, neigh_db):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    for inst in neigh_db:
        insertion = (inst[0], inst[1])
        statement = 'INSERT INTO "Neighborhoods" '
        statement += 'VALUES (?, ?)'
        cur.execute(statement, insertion)
    # print('insert neighborhoods data.')

    for inst in bar_db:
        insertion = (None, inst[0], float(inst[1]), inst[2], inst[3],
                     inst[4], inst[5], inst[6], inst[7], float(inst[8]))
        statement = 'INSERT INTO "Bars" '
        statement += 'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?,?)'
        cur.execute(statement, insertion)

    # print('insert bar data')
    conn.commit()
    conn.close()


def insert_calc_neigh():
    ''' 
    Add the number of bars and average bar price rating to the neighborhoods.
    '''
    # start the connection
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    # calculate bar number, price ratings for each neighborhood
    bar_statement = '''
    SELECT Neighborhood, count(Id) as Bar_num, round(avg(Price),2) as Avg_Price
    FROM Bars
    GROUP by Neighborhood
    '''

    cur.execute(bar_statement)
    conn.commit()
    output = cur.fetchall()  # list of tuples

    # update the neighborhoods column with new columns
    statement = '''
    ALTER TABLE Neighborhoods 
    ADD COLUMN "Bar_Num" INT;
    '''
    cur.execute(statement)
    conn.commit()

    statement = '''
    ALTER TABLE Neighborhoods 
    ADD COLUMN "Avg_Price" REAL;
    '''
    cur.execute(statement)
    conn.commit()

    # insert data into neighborhoods db
    for inst in output:
        statement = '''
        UPDATE Neighborhoods
        SET Bar_Num = ''' + str(inst[1]) + ''', Avg_Price= ''' + str(inst[2])+'''
        WHERE Id = ''' + str(inst[0])
        cur.execute(statement)

    conn.commit()
    conn.close()


def update_neigh_csv():
    # reference: https://stackoverflow.com/questions/18827028/write-to-csv-from-sqlite3-database-in-python
    with sqlite3.connect("nycbars.db") as connection:
        csvWriter = csv.writer(open("data/neighborhoods.csv", "w"))
        # add header
        fieldnames = ['id', 'name', 'bar_num', 'avg_price']
        # writer = csv.DictWriter(bars, fieldnames=fieldnames)
        csvWriter.writerow(fieldnames)

        cur = connection.cursor()

        statement = '''
        SELECT * 
        FROM Neighborhoods
        '''
        cur.execute(statement)
        connection.commit()
        rows = cur.fetchall()
        csvWriter.writerows(rows)


(barls, neighls) = get_bars()
neigh_dic = get_neigh(neighls)
for bar in barls:
    bar.set_neigh(neigh_dic)  # update the foreign key

create_bar_csv(barls)
create_neigh_csv(neigh_dic)


bar_db = read_csv_to_db(BARSCSV, 'name')
neigh_db = read_csv_to_db(NEIGHBORCSV, 'id')

init_db()
insert_data(bar_db, neigh_db)


insert_calc_neigh()
update_neigh_csv()
