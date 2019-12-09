# model.py
import csv

NB_FILE_NAME = 'data/neighborhoods.csv'
BAR_FILE_NAME = 'data/bars.csv'

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
