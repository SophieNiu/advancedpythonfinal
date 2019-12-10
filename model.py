# model.py
import csv
import sqlite3

DBNAME = 'nycbars.db'
NB_FILE_NAME = 'data/neighborhoods.csv'
BAR_FILE_NAME = 'data/bars_info.csv'

neighbors = []


def init_neighbors(csv_file_name=NB_FILE_NAME):
    global neighbors
    with open(csv_file_name) as f:
        reader = csv.reader(f)
        next(reader)  # throw away headers
        neighbors = []  # reset, start clean
        for r in reader:
            r[2] = int(r[2])
            r[3] = float(r[3])
            neighbors.append(r)


def get_neighbors(sortby='bar_num', sortorder='desc'):
    if sortby == 'bar_num':
        sortcol = 2
    elif sortby == 'avg_price':
        sortcol = 3
    elif sortby == 'alphabetical':
        sortcol = 1
    else:
        sortcol = 0

    rev = (sortorder == 'desc')
    sorted_list = sorted(neighbors, key=lambda row: row[sortcol], reverse=rev)
    return sorted_list


def get_filtered_bars(nid=0):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    statement = '''
    SELECT Name,Price,Website, Phone,Address,NeighName
    FROM Bars JOIN Neighborhoods 
    ON Bars.Neighborhood= Neighborhoods.Id
    '''
    if nid != 0:
        statement += '''WHERE Neighborhoods.Id = ''' + str(nid)

    cur.execute(statement)
    filtered_bars = cur.fetchall()  # list of tuples
    conn.commit()
    conn.close()
    return filtered_bars
