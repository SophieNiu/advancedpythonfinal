# model.py
import csv

NB_FILE_NAME = 'data/neighborhoods.csv'

bb_seasons = []


def init_bball(csv_file_name=BB_FILE_NAME):
    global bb_seasons
    with open(csv_file_name) as f:
        reader = csv.reader(f)
        next(reader)  # throw away headers
        next(reader)  # throw away headers
        bb_seasons = []  # reset, start clean
        for r in reader:
            r[3] = int(r[3])
            r[4] = int(r[4])
            r[5] = float(r[5])
            bb_seasons.append(r)


def get_bball_seasons(sortby='year', sortorder='desc'):
    if sortby == 'year':
        sortcol = 1
    elif sortby == 'wins':
        sortcol = 3
    elif sortby == 'pct':
        sortcol = 5
    else:
        sortcol = 0

    rev = (sortorder == 'desc')
    sorted_list = sorted(bb_seasons, key=lambda row: row[sortcol], reverse=rev)
    return sorted_list
