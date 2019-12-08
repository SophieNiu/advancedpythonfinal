import sqlite3
import csv
import json
import sys
import re


# proj3_choc.py
# You can change anything in this file you want as long as you pass the tests
# and meet the project requirements! You will need to implement several new
# functions.

# Part 1: Read data from CSV and JSON into a new database called choc.db
DBNAME = 'choc.db'
BARSCSV = 'flavors_of_cacao_cleaned.csv'
COUNTRIESJSON = 'countries.json'

# Read bar csv file to lists
fn = open(BARSCSV)
csv_data = csv.reader(fn)
bar_data = []
for row in csv_data:
    if row[0] != "Company":
        bar_data.append(row)

# print(bar_data[0])

# Read json file to lists
country_data = []

with open(COUNTRIESJSON) as json_file:
    data = json.load(json_file)

for i in data:
    country = [i["alpha2Code"], i["alpha3Code"],
               i["name"], i["region"], i["subregion"], i["population"], i["area"]]
    country_data.append(country)


def init_db():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    # Drop tables
    statement = '''
        DROP TABLE IF EXISTS 'Bars';
    '''
    cur.execute(statement)
    statement = '''
        DROP TABLE IF EXISTS 'Countries';
    '''
    cur.execute(statement)

    conn.commit()

    statement = '''
        CREATE TABLE "Bars" (
        "Id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        "Company"	TEXT,
        "SpecificBeanBarName"	TEXT,
        "REF"	TEXT,
        "ReviewDate"	TEXT,
        "CocoaPercent"	REAL,
        "CompanyLocationId"	INTEGER NOT NULL,
        "Rating"	REAL,
        "BeanType"	TEXT,
        "BroadBeanOriginId" INTEGER,
        FOREIGN KEY (CompanyLocationId) REFERENCES Countries(Id),
		FOREIGN KEY (BroadBeanOriginId) REFERENCES Countries(Id)
    	);

        '''

    cur.execute(statement)
    # print('create Bars table')

    statement = '''
        CREATE TABLE "Countries" (
	    "Id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	    "Alpha2"	TEXT,
	    "Alpha3"	TEXT,
	    "EnglishName"	TEXT,
	    "Region"	TEXT,
	    "Subregion"	TEXT,
	    "Population"	INTEGER,
	    "Area"	REAL
        );

        '''
    cur.execute(statement)
    # print('create countries table')
    conn.commit()
    conn.close()


def insert_data():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    for inst in country_data:
        insertion = (None, inst[0], inst[1], inst[2], inst[3],
                     inst[4], inst[5], inst[6])
        statement = 'INSERT INTO "Countries" '
        statement += 'VALUES (?, ?, ?, ?, ?, ?, ?, ?)'
        cur.execute(statement, insertion)
    # print('insert country data.')

    country_name = {}
    statement = '''
    SELECT EnglishName, Id FROM Countries
    '''
    cur.execute(statement)
    result = cur.fetchall()
    for row in result:
        country_name[row[0]] = row[1]
        # print(type(row[1]))

    for inst in bar_data:
        # inst[5], inst[8] needs int, need to find the countries id in the countries table
        country_location = country_name[inst[5]]
        try:
            country_origin = country_name[inst[8]]
        except:
            country_origin = 'NULL'
        cocoa = float(float(inst[4].split('%')[0])/100)
        # print(type(cocoa))

        insertion = (None, inst[0], inst[1], inst[2], inst[3],
                     cocoa, country_location, float(inst[6]), inst[7], country_origin)
        statement = 'INSERT INTO "Bars" '
        statement += 'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?,?)'
        cur.execute(statement, insertion)
        # except:
        #     print('KeyError')
    # print('insert bar data')
    conn.commit()
    conn.close()

# Part 2: Implement logic to process user commands


def process_command(command):
    # Create a list of commands/ triggers to different queries
    commands = command.split(' ')
    statement = ''''''
    # Start the connection
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    # create the default statement for order and statement to update and append to the select statement
    order_st = "ORDER by b.Rating "
    limit_st = "DESC LIMIT 10"

    if commands[0] == "bars":
        # Set up the initial select statement
        statement = '''
        SELECT b.SpecificBeanBarName, b.Company, comploc.EnglishName, b.Rating, b.CocoaPercent, origin.EnglishName
        FROM Countries as comploc JOIN Bars as b
	    on comploc.Id = b.CompanyLocationId
	    LEFT JOIN Countries as origin 
	    on origin.Id = b.BroadBeanOriginId 

        '''
        for command in commands[1:]:
            try:
                c_key = command.split('=')[0]
                c_val = command.split('=')[1]
                # first command section for where statement
                if c_key == "sellcountry":
                    statement += """WHERE comploc.Alpha2='"""+c_val+"' "
                elif c_key == "sourcecountry":
                    statement += """WHERE origin.Alpha2='"""+c_val+"' "
                elif c_key == "sellregion":
                    statement += """WHERE comploc.Region='"""+c_val+"' "
                elif c_key == "sourceregion":
                    statement += """WHERE origin.Region='"""+c_val+"' "
                elif c_key == "top":
                    limit_st = "DESC LIMIT " + c_val
                    # statement.replace("LIMIT 10", limit_st)
                elif c_key == "bottom":
                    limit_st = "LIMIT " + c_val
                    # statement.replace("LIMIT 10", limit_st)
            except:
                if command == 'cocoa':
                    order_st = 'Order by b.CocoaPercent '
                # statement.replace("Order by b.Rating", order_st)
                # ratings is the default so I don't need to replace the order statement

        # Combine the statement based on the commands
        statement += order_st + limit_st

        # print(statement)

    if commands[0] == "companies":
        # Set up the initial select statement
        agg = ''
        loc_st = ''
        select_st = '''SELECT b.Company, comploc.EnglishName '''

        # Filter companies based on bars count
        from_st = '''
            FROM Countries as comploc JOIN Bars as b
	        on comploc.Id = b.CompanyLocationId
            '''
        group_st = '''GROUP by b.Company
	                HAVING count(b.SpecificBeanBarName)>4
        '''
        for command in commands[1:]:
            try:
                c_key = command.split('=')[0]
                c_val = command.split('=')[1]
                # first command section for where statement
                if c_key == "country":
                    loc_st = """WHERE comploc.Alpha2='""" + c_val+"' "
                elif c_key == "region":
                    loc_st = """WHERE comploc.Region='""" + c_val+"' "

                # Update limit statement
                elif c_key == "top":
                    limit_st = "DESC LIMIT " + c_val
                    # statement.replace("LIMIT 10", limit_st)
                elif c_key == "bottom":
                    limit_st = "LIMIT " + c_val
                    # statement.replace("LIMIT 10", limit_st)

            except:
                if command == 'cocoa':
                    # CocoaPercent is input as str, need to convert to int for calculation
                    agg = 'round(avg(b.CocoaPercent),2)'
                    select_st += ', ' + agg
                    order_st = 'ORDER by avg(b.CocoaPercent) '

                elif command == 'ratings':
                    agg = 'round(b.Rating,1)'
                    select_st += ', ' + agg
                    order_st = 'ORDER by avg(b.Rating) '

                elif command == 'bars_sold':
                    agg = 'count(b.SpecificBeanBarName)'
                    select_st += ', ' + agg
                    order_st = 'ORDER by count(b.SpecificBeanBarName)'

        statement = select_st + from_st + loc_st + group_st + order_st + limit_st
        # print(statement)

    if commands[0] == "countries":
        # Set up the initial select statement
        agg = ''
        loc_st = ''

        # Filter companies based on bars count
        join_st = '''
            FROM Countries as comploc JOIN Bars as b
	        on comploc.Id = b.CompanyLocationId
	        LEFT JOIN Countries as origin 
	        on origin.Id = b.BroadBeanOriginId 
        '''

        group_st = '''
            GROUP by comploc.Id
	        HAVING count(b.Id) >4 
        '''
        for command in commands[1:]:
            try:
                c_key = command.split('=')[0]
                c_val = command.split('=')[1]
                # first command section for where statement
                if c_key == "region":
                    loc_st = """WHERE comploc.Region='"""+c_val+"' "

                # Update limit statement
                elif c_key == "top":
                    limit_st = "DESC LIMIT " + c_val
                    # statement.replace("LIMIT 10", limit_st)
                elif c_key == "bottom":
                    limit_st = "LIMIT " + c_val
                    # statement.replace("LIMIT 10", limit_st)

            except:
                if command == 'cocoa':
                    # CocoaPercent is input as str, need to convert to int for calculation
                    agg = 'round(avg(b.CocoaPercent),2)'
                    select_st = '''SELECT DISTINCT comploc.EnglishName, comploc.Region, ''' + agg
                    order_st = 'ORDER by avg(b.CocoaPercent) '

                elif command == 'ratings':
                    agg = 'round(b.Rating,1)'
                    select_st = '''SELECT DISTINCT comploc.EnglishName, comploc.Region,  ''' + agg
                    order_st = 'ORDER by avg(b.Rating) '

                elif command == 'bars_sold':
                    agg = 'count(b.SpecificBeanBarName)'
                    select_st = '''SELECT DISTINCT comploc.EnglishName, comploc.Region, ''' + agg
                    order_st = 'ORDER by count(b.SpecificBeanBarName)'

                # by default is selecting from sellers
                elif command == "sellers":
                    group_st = '''GROUP by comploc.Id
                                    HAVING count(Bars.Id) >4'''

                elif command == "sources":
                    group_st = '''GROUP by origin.Id
	                            HAVING count(Bars.Id) >4'''

        statement = select_st + join_st + loc_st + group_st + order_st + limit_st
        # print(statement)

    if commands[0] == "regions":
        # Set up the initial select statement
        agg = ''
        loc_st = ''
        select_st = '''SELECT DISTINCT comploc.Region '''

        # Filter companies based on bars count
        join_st = '''
            FROM Countries as comploc JOIN Bars as b
	        on comploc.Id = b.CompanyLocationId
	        LEFT JOIN Countries as origin 
	        on origin.Id = b.BroadBeanOriginId 
        '''

        group_st = '''
            GROUP by comploc.Region
	        HAVING count(b.Id) >4 
        '''
        for command in commands[1:]:
            try:
                c_key = command.split('=')[0]
                c_val = command.split('=')[1]
                # Update limit statement
                if c_key == "top":
                    limit_st = "DESC LIMIT " + c_val
                    # statement.replace("LIMIT 10", limit_st)
                elif c_key == "bottom":
                    limit_st = "LIMIT " + c_val
                    # statement.replace("LIMIT 10", limit_st)

            except:
                if command == 'cocoa':
                    # CocoaPercent is input as str, need to convert to int for calculation
                    agg = 'round(avg(b.CocoaPercent),2) '
                    select_st += ''', ''' + agg
                    order_st = 'ORDER by avg(b.CocoaPercent) '

                elif command == 'ratings':
                    agg = 'round(b.Rating,1)'
                    select_st += ''', ''' + agg
                    order_st = 'ORDER by avg(b.Rating) '

                elif command == 'bars_sold':
                    agg = 'count(b.SpecificBeanBarName) '
                    select_st += ''', ''' + agg
                    order_st = 'ORDER by count(b.SpecificBeanBarName) '

                # by default is selecting from sellers
                elif command == "sellers":
                    group_st = '''GROUP by comploc.Region
                                    HAVING count(b.Id) >4 '''

                elif command == "sources":
                    group_st = '''GROUP by origin.Region
	                            HAVING count(b.Id) >4 '''

        statement = select_st + join_st + loc_st + group_st + order_st + limit_st
        # print(statement)

    cur.execute(statement)
    conn.commit()
    output = cur.fetchall()
    conn.close()
    return output


def load_help_text():
    with open('help.txt') as f:
        return f.read()

# Part 3: Implement interactive prompt. We've started for you!


def interactive_prompt():
    help_text = load_help_text()
    response = ''
    params = ['bars','companies','countries','regions','region','ratings','cocoa','bottom','top','sellcountry','sourcecountry','sellregion','sourceregion','country','sellers','sources','help','exit']
    while response != 'exit':
        response = input('Enter a command: ')
        strs = response.split(' ')

        try: 
            for s in strs: 
                if (s or s.split('=')[0]) not in params: 
                    print('Sorry, I could not understand your command: ' +
                          response + '. Could you try something else?')
        except: 
            results = process_command(response)
            for item in results:
                row = ''
                for i in item:
                    if len(str(i)) < 15:
                        row += str(i) + ' ' * (15-len(str(i)))
                    else:
                        row += str(i[:12]) + '...'
                print(row)
        
        if response == 'help':
            print(help_text)
            continue
    print('Bye!')


# Make sure nothing runs or prints out when this file is run as a module
if __name__ == "__main__":
    init_db()

    if len(sys.argv) > 1 and sys.argv[1] == '--init':
        print('Deleting db and starting over from scratch.')
        init_db()
    else:
        print('Leaving the DB alone.')

    insert_data()

    interactive_prompt()
