import sqlite3
import csv
import json

# proj3_choc.py
# You can change anything in this file you want as long as you pass the tests
# and meet the project requirements! You will need to implement several new
# functions.

# Part 1: Read data from CSV and JSON into a new database called choc.db
DBNAME = 'choc.db'
BARSCSV = 'flavors_of_cacao_cleaned.csv'
COUNTRIESJSON = 'countries.json'


f=open(BARSCSV)
csv_data=csv.reader(f)

Company=[]
BeanBarName=[]
REF=[]
ReviewDate=[]
CocoaPercent=[]
CompanyLocation=[]
Rating=[]
BeanType=[]
BroadBeanOrigin=[]


for row in csv_data:
	if row[0]!="Company":
		Company.append(row[0])
		BeanBarName.append(row[1])
		REF.append(row[2])
		ReviewDate.append(row[3])
		CocoaPercent.append(row[4])
		CompanyLocation.append(row[5])
		Rating.append(row[6])
		BeanType.append(row[7])
		BroadBeanOrigin.append(row[8])
	else:
		pass

Alpha2=[]
Alpha3=[]
EnglishName=[]
Region=[]
Subregion=[]
Population=[]
Area=[]

with open('countries.json') as json_file:
	data=json.load(json_file)
for i in data:
	Alpha2.append(i["alpha2Code"])
	Alpha3.append(i["alpha3Code"])
	EnglishName.append(i["name"])
	Region.append(i["region"])
	Subregion.append(i["subregion"])
	Population.append(i["population"])
	Area.append(i["area"])



def create_table():
	conn = sqlite3.connect(DBNAME)
	cur = conn.cursor()
	cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='Countries' ''')
	result = cur.fetchone()
	if result[0]==1:
		print ("table Countries has been created.")
	else:
		statement="""
		CREATE TABLE 'Countries' (
	  'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
	  'Alpha2' TEXT varchar(2),
	  'Alpha3' TEXT varchar(3),
	  'EnglishName' text,
	  'Region' TEXT,
	  'Subregion' Real,
	  'Population' Integer,
	  'Area' Real
	); 

	"""
		cur.execute(statement)
		conn.commit()
		print ("Table Countries just created.")

	cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='Bars' ''')
	result = cur.fetchone()
	if result[0]==1:
		print ("table Bars has been created.")
	else:
		statement="""
		CREATE TABLE Bars (
		Id INTEGER PRIMARY KEY AUTOINCREMENT,
		Company TEXT,
		SpecificBeanBarName TEXT,
		REF INTEGER,
		ReviewDate TEXT,
		CocoaPercent REAL,
		CompanyLocationId INT    NOT NULL,
				Rating Real,
		BeanType Text,
		BroadBeanOriginId int not null,
		FOREIGN KEY (CompanyLocationId) REFERENCES Countries(Id),
		FOREIGN KEY (BroadBeanOriginId) REFERENCES Countries(Id)
		); 

		"""
		cur.execute(statement)
		conn.commit()
		print ("Table Bars just created.")



	conn.close()


# create_table()

def insert_stuff():
	conn = sqlite3.connect(DBNAME)
	cur = conn.cursor()
	# clean the db before inserting any data

	delete_stmt="DELETE FROM Countries"
	cur.execute(delete_stmt)
	conn.commit()
# insert data to countries

	for i in range(len(EnglishName)):
		insertion = (None, Alpha2[i], Alpha3[i], EnglishName[i], Region[i],
		Subregion[i],Population[i],Area[i])
		statement='INSERT INTO "Countries" '
		statement+='VALUES(?,?,?,?,?,?,?,?)'
		cur.execute(statement, insertion)

	conn.commit()

	return_dict={}
	result = cur.execute("select EnglishName,ID from Countries")
	for row in result:
		return_dict[row[0]] = row[1]

	delete_stmt="DELETE FROM Bars"
	cur.execute(delete_stmt)
	conn.commit()
	for i in range(len(Company)):
		CompanyLocation_text=CompanyLocation[i]
		BroadBeanOrigin_text=BroadBeanOrigin[i]
		try:
			insertion = (None, Company[i], BeanBarName[i], REF[i], ReviewDate[i],
				float(float(CocoaPercent[i].split("%")[0])/100),return_dict[CompanyLocation_text],Rating[i], BeanType[i],
				return_dict[BroadBeanOrigin_text])
			statement='INSERT INTO "Bars" '
			statement+='VALUES(?,?,?,?,?,?,?,?,?,?)'
			cur.execute(statement, insertion)
		except:
			insertion = (None, Company[i], BeanBarName[i], REF[i], ReviewDate[i],
				float(float(CocoaPercent[i].split("%")[0])/100),return_dict[CompanyLocation_text],Rating[i], BeanType[i],
				"Null")
			statement='INSERT INTO "Bars" '
			statement+='VALUES(?,?,?,?,?,?,?,?,?,?)'
			cur.execute(statement, insertion)

	conn.commit()
	conn.close()


create_table()
insert_stuff()


# Part 2: Implement logic to process user commands
def process_command(command):
	output=[]
	conn = sqlite3.connect(DBNAME)
	cur = conn.cursor()
	command_lst=command.split(" ")
	agg=""
	join_statement="""
					join Bars as b
					on b.CompanyLocationId=c.id """
	end_statement="desc limit 10 "
	where_statement=""
	order_statement="order by b.Rating "
	statement=''

	if command_lst[0]=="bars":
		statement="""SELECT b.SpecificBeanBarName, b.Company, c.EnglishName, b.Rating, b.CocoaPercent, 
					c1.EnglishName
					from Bars as b 
					join Countries as c
					on b.CompanyLocationId=c.id
					join Countries as c1
					on c1.Id=b.BroadBeanOriginId """
		for i in command_lst[1:]:
			try:
				key=i.split("=")[0]
				value=i.split("=")[1]
				if key=="sellcountry":
					statement+="""
					where c.Alpha2='"""+value+"' "
				elif key=="sourcecountry":
					statement+="""
					where c1.Alpha2='"""+value+"' "
				elif key=="sourcecountry":
					statement+="""
					where c.Region='"""+value+"' "
				elif key=="sourceregion":
					statement+="""
					where c1.Region='"""+value+"' "
				elif key=="top":
					end_statement="desc limit "+value
				elif key=="bottom":
					end_statement="limit "+value

				
			except:
				if i=="ratings":
					order_statement="order by b.Rating "
				elif i=="cocoa":
					order_statement="order by b.CocoaPercent "

		statement+=order_statement+end_statement

	# coutnries table 

	if command_lst[0]=="companies":
		group_by_statement="""group by b.Company
					having count(b.specificBeanBarName)>4 """
		for i in command_lst[1:]:
			try:
				key=i.split("=")[0]
				value=i.split("=")[1]
				if key=="region":
					where_statement+="""where c.Region='"""+value+"' "
				elif key=="country":
					where_statement+="""where c.Alpha2='"""+value+"' "
				elif key=="top":

					end_statement="desc limit "+value
				elif key=="bottom":
					end_statement="limit "+value

				
			except:
				if key=="sellers":
					statement+="""
					join Countries as c1
					on b.CompanyLocationId=c1.id """
				elif key=="sources":
					statement+="""
					join Countries as c1
					on b.BroadBeanOriginId=c1.id """
				elif i=="ratings":
					agg="b.Rating"
					statement="SELECT b.Company, c.EnglishName, AVG("+agg+")"
					statement+=""" from Bars as b 
					join Countries as c
					on b.CompanyLocationId=c.id """
					order_statement="order by AVG(b.Rating) "	
				elif i=="bars_sold":
					agg="count(b.specificBeanBarName)"
					statement="SELECT b.Company, c.EnglishName, "+agg
					statement+=""" from Bars as b 
					join Countries as c
					on b.CompanyLocationId=c.id """
					order_statement="order by count(b.specificBeanBarName) "
				elif i=="cocoa":
					agg="b.CocoaPercent"
					statement="SELECT b.Company, c.EnglishName, AVG("+agg+")"
					statement+=""" from Bars as b 
					join Countries as c
					on b.CompanyLocationId=c.id """					
					order_statement="order by AVG(b.CocoaPercent) "
		statement+=where_statement+group_by_statement+order_statement+end_statement

				# command countries
	if command_lst[0]=="countries":
		group_by_statement="""group by c.EnglishName
					having count(b.specificBeanBarName)>4 """
		order_statement=""
		for i in command_lst[1:]:
			try:
				key=i.split("=")[0]
				value=i.split("=")[1]
				if key=="region":
					where_statement+=""" where c.Region='"""+value+"' "
				elif key=="top":
					end_statement="desc limit "+value
				elif key=="bottom":
					end_statement="limit "+value


				
			except:
				if key=="sellers":
					join_statement="""
					join Bars as b
					on b.CompanyLocationId=c.id """
				elif key=="sources":
					join_statement="""
					join Bars as b
					on b.BroadBeanOriginId=c.id """
				elif i=="ratings":
					agg="b.Rating"
					statement="SELECT c.EnglishName, c.Region, AVG("+agg+")"+ " from Countries as c "
					order_statement="order by AVG(b.Rating) "	
				elif i=="bars_sold":
					agg="count(b.specificBeanBarName)"
					statement="SELECT c.EnglishName, c.Region, "+agg+ " from Countries as c "
					order_statement="order by count(b.specificBeanBarName) "
				elif i=="cocoa":
					agg="b.CocoaPercent"
					statement="SELECT c.EnglishName, c.Region, AVG("+agg+")"+ " from Countries as c "
					order_statement="order by AVG(b.CocoaPercent) "
		statement+=join_statement+where_statement+group_by_statement+order_statement+end_statement
# commans region 
	if command_lst[0]=="regions":
		group_by_statement="""group by c.Region
					having count(b.specificBeanBarName)>4 """
		for i in command_lst[1:]:
			try:
				key=i.split("=")[0]
				value=i.split("=")[1]
				if key=="top":
					end_statement="desc limit "+value
				elif key=="bottom":
					end_statement="limit "+value

				
			except:
				if key=="sellers":
					join_statement="""
					join Bars as b
					on b.CompanyLocationId=c.id """
				elif key=="sources":
					join_statement="""
					join Bars as b
					on b.BroadBeanOriginId=c.id """
				elif i=="ratings":
					agg="b.Rating"
					statement="SELECT c.Region, AVG("+agg+")"+ " from Countries as c "
					order_statement="order by AVG(b.Rating) "	
				elif i=="bars_sold":
					agg="count(b.specificBeanBarName)"
					statement="SELECT c.Region, "+agg+ " from Countries as c "
					order_statement="order by count(b.specificBeanBarName) "
				elif i=="cocoa":
					agg="b.CocoaPercent"
					statement="SELECT c.Region, AVG("+agg+")"+ " from Countries as c "
					order_statement="order by AVG(b.CocoaPercent) "

		statement+=join_statement+where_statement+group_by_statement+order_statement+end_statement
	# print (statement)
	results=cur.execute(statement)
	conn.commit()
	results=results.fetchall()
	conn.close()
	return results


def load_help_text():
	with open('help.txt') as f:
		return f.read()

# Part 3: Implement interactive prompt. We've started for you!
def interactive_prompt():
	help_text = load_help_text()
	response = ''
	while response.lower() != 'exit':
		response = input('Enter a command, "help", or "exit": ')
		if response.lower() == 'help':
			print(help_text)
			continue
			# check input
		elif response.lower() == 'exit':
			print ("Bye.")
			break
		else:
			if process_command(response)==[]:
				print ("No data returned. Please check your input or try again.")
			else:
				output=process_command(response)
				print_row=" "
				for row in output:
					print_row=""
					for text in row:
						if type(text) is float:
							print_row+='{0: <15}'.format(round(text,1))+" "
						elif len(str(text).strip(""))<12:
							print_row+='{0: <15}'.format(text)+" "
						else:
							print_row+='{0: <12}'.format(str(text)[:12])+"... "
					print (print_row)

# Make sure nothing runs or prints out when this file is run as a module
if __name__=="__main__":
    interactive_prompt()
