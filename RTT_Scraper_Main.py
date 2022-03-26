from datetime import date
import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3 as sl
import asyncio
from tqdm import tqdm

def options ():
    print('Add data to databases = 1 | Query Databases = 2 | Exit = 3 ')
    option = input() 

    while option != '1' and option != '2' and option != '3': 
        print('Add data to databases = 1 | Query Databases = 2 | Exit = 3 ')
        option = input()
        
    if option == '1': 
        pass
    elif option == '2':
        from DB_Query import db
    else:
        exit()

options()
links = []
headers = []
allox = []
allox_more = []
n = 9
m = 21

file_path = "Stations.xlsx"
df = pd.read_excel(file_path)
user_station = input("Please enter a station name: ")
a = df["CRS Code"].where(df["Station Name"] == user_station)
b = (a.dropna())
c = b.to_string(index=False)

today = date.today()
d = today.strftime("%Y-%m-%d")

def no_toc():
    global URL
    URL = "https://www.realtimetrains.co.uk/search/detailed/gb-nr:" + c + "/" + d + "/0000-2359?stp=WVS&show=all&order=wtt"



no_toc()

page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')

for a in soup.find_all('a', href=True):
    hrefs = a['href']
    links.append(hrefs)

del links[:n]
del links[-m:]

async def scraper():
    print("Getting information...")
    for x in tqdm(range(0, len(links))):
        formatted_link = ("https://www.realtimetrains.co.uk" + links[x])
        page_links = requests.get(formatted_link)
        global page_soup
        page_soup = BeautifulSoup(page_links.content, 'html.parser')
        task1 = asyncio.create_task(find_header())
        task2 = asyncio.create_task(find_allox())
        await task1
        await task2


async def find_header():
    global header
    header = page_soup.find(class_='header')
    apostrophe = "'"
    header_search = header.text
    if apostrophe in header_search:
        header = header_search.replace("'", "")
        global contained_apostrophe
        contained_apostrophe = True
    else:
        contained_apostrophe = False
    if contained_apostrophe is False:
        headers.append(header.text)
    elif contained_apostrophe is True:
        headers.append(header)

async def find_allox():
    results = page_soup.find(class_='allocation')
    if results == None:
        allox.append("No allox")
    else:
        changes = len(results.find_all("ul"))
        if changes == 0:
            allox.append(results.string)
        elif changes == 1:
            for p in results.find_all('li'):
                allox_more.append(p.text)
            joined = (" ".join(allox_more))
            allox.append(joined)
            allox_more.clear()

asyncio.run(scraper())

con = sl.connect("Databases/" + user_station + '.db')
cursor = con.cursor()

res = " " in user_station

if res is True:
    table_station = user_station.replace(" ", "_")
    open_b = "("
    close_b = ")"
    if open_b and close_b in table_station:
        table_station = table_station.replace("(", "")
        table_station = table_station.replace(")", "")
    else:
        pass
    table_date = d.replace("-", "_")
    table_name = table_station + "_" + table_date
else:
    table_date = d.replace("-", "_")
    table_name = user_station + "_" + table_date

def insert():
    print("Adding data to " + user_station + ".db")
    for x in tqdm(range(0, len(links))):
        sql = "INSERT INTO " + table_name + " (service, allox, date) values(?, ?, ?)"
        data = [
            (headers[x], allox[x], d)
        ]
        with con:
            con.executemany(sql, data)

def replace():
    print("Updating data in " + user_station + ".db")
    sql_clear_table = "DELETE FROM " + table_name
    with con:
            con.execute(sql_clear_table)
            
    sql_reset_id = "UPDATE sqlite_sequence SET seq='0' WHERE name= '" + table_name + "'" 
    with con:
        con.execute(sql_reset_id)
    for x in tqdm(range(0, len(links))):
        sql_insert = "INSERT INTO " + table_name + " (service, allox, date) values(?, ?, ?)"
        data = [
            (headers[x], allox[x], d)
        ]
        with con:
            con.executemany(sql_insert, data)
        

tab_sql = ("SELECT name FROM sqlite_master WHERE type='table' AND name='" + table_name + "'")

cursor.execute(tab_sql)
table_result = cursor.fetchall()

if table_result:
    replace()
else:
    con.execute("CREATE TABLE " + table_name + " (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, service TEXT, allox TEXT, date TEXT)")
    insert()

options()