from datetime import date
import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3 as sl
import asyncio
from tqdm import tqdm

def main():
    while True:
        def options ():
            print('Add data to databases = 1 | Query Databases = 2 | Exit = 3 ')
            option = input() 

            while option != '1' and option != '2' and option != '3': 
                print('Add data to databases = 1 | Query Databases = 2 | Exit = 3 ')
                option = input()
                
            if option == '1': 
                return
            elif option == '2':
                db()
            else:
                exit()

        options()
        links = []
        headers = []
        allox = []
        allox_more = []
        remove_hrefs_before = 9
        remove_hrefs_after = 21

        file_path = "Stations.xlsx"
        station_df = pd.read_excel(file_path)
        user_station = input("Please enter a station name: ")
        a = station_df["CRS Code"].where(station_df["Station Name"] == user_station)
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

        del links[:remove_hrefs_before]
        del links[-remove_hrefs_after:]

        async def scraper():
            print("Getting information...")
            for x in tqdm(range(0, len(links))):
                formatted_link = ("https://www.realtimetrains.co.uk" + links[x])
                page_links = requests.get(formatted_link)
                global page_soup
                page_soup = BeautifulSoup(page_links.content, 'html.parser')
                get_header = asyncio.create_task(find_header())
                get_allox = asyncio.create_task(find_allox())
                await get_header
                await get_allox


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
            allocation = page_soup.find(class_='allocation')
            if allocation == None:
                allox.append("No allox")
            else:
                changes = len(allocation.find_all("ul"))
                if changes == 0:
                    allox.append(allocation.string)
                elif changes == 1:
                    for p in allocation.find_all('li'):
                        allox_more.append(p.text)
                    joined = (" ".join(allox_more))
                    allox.append(joined)
                    allox_more.clear()

        asyncio.run(scraper())

        con = sl.connect("Databases/" + user_station + '.db')
        cursor = con.cursor()

        space = " " in user_station
        open_b = "(" in user_station
        close_b = ")" in user_station
        dash = "-" in user_station
        apos = "'" in user_station
        andsymbol = "&" in user_station

        if space is True and open_b is False and close_b is False and dash is False and apos is False and andsymbol is False:
            table_station = user_station.replace(" ", "_")
            table_date = d.replace("-", "_")
            table_name = table_station + "_" + table_date
        elif space is True and open_b is True and close_b is True and dash is False and apos is False and andsymbol is False:
            table_station = user_station.replace(" ", "_").replace("(", "").replace(")", "")
            table_date = d.replace("-", "_")
            table_name = table_station + "_" + table_date
        elif space is False and open_b is False and close_b is False and dash is True and apos is True and andsymbol is False:
            table_station = user_station.replace("-", "_").replace("'", "_")
            table_date = d.replace("-", "_")
            table_name = table_station + "_" + table_date
        elif space is False and open_b is False and close_b is False and dash is True and apos is False and andsymbol is False:
            table_station = user_station.replace("-", "_")
            table_date = d.replace("-", "_")
            table_name = table_station + "_" + table_date
        elif space is True and open_b is False and close_b is False and dash is False and apos is True and andsymbol is True:
            table_station = user_station.replace("'", "").replace(" ", "_").replace("&", "")
            table_date = d.replace("-", "_")
            table_name = table_station + "_" + table_date
        elif space is True and open_b is False and close_b is False and dash is False and apos is True and andsymbol is False:
            table_station = user_station.replace(" ", "_").replace("'", "")
            table_date = d.replace("-", "_")
            table_name = table_station + "_" + table_date
        elif space is True and open_b is False and close_b is False and dash is False and apos is False and andsymbol is True:
            table_station = user_station.replace(" ", "_").replace("&", "")
            table_date = d.replace("-", "_")
            table_name = table_station + "_" + table_date
        else:
            table_date = d.replace("-", "_")
            table_name = user_station + "_" + table_date

        def insert():
            print("Adding data to " + user_station + ".db")
            for x in tqdm(range(0, len(links))):
                sql_add = "INSERT INTO " + table_name + " (service, allox, date) values(?, ?, ?)"
                data = [
                    (headers[x], allox[x], d)
                ]
                with con:
                    con.executemany(sql_add, data)

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
                

        table_sql = ("SELECT name FROM sqlite_master WHERE type='table' AND name='" + table_name + "'")

        cursor.execute(table_sql)
        table_result = cursor.fetchall()

        if table_result:
            replace()
        else:
            con.execute("CREATE TABLE " + table_name + " (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, service TEXT, allox TEXT, date TEXT)")
            insert()
        
def db():
    global tn
    tn = []
    station_name = input("Please enter a station name you would like to query: ")
    con = sl.connect("Databases/" + station_name + ".db")
    global cursor
    cursor = con.cursor()

    res = con.execute("SELECT name FROM sqlite_master WHERE type='table';")
    for name in res.fetchall():
        tn.append(name[0])

    tn.remove("sqlite_sequence")

    search()

def search_allox():
    user_allox = input("Enter Loco/Unit Number: ")
    for x in range(0, len(tn)):
        cursor.execute("SELECT * FROM " + tn[x] + " WHERE allox LIKE '%" + user_allox + "%'")
        for allox in cursor.fetchall():
            print(allox)

    search_again()

def search_service():
    user_service = input("Enter service detail: ")
    for x in range(0, len(tn)):
        cursor.execute("SELECT * FROM " + tn[x] + " WHERE service LIKE '%" + user_service + "%'")
        for service in cursor.fetchall():
            print(service)
    
    search_again()

def search():
    while True:
        user_choice = input("1. Search by Loco/Unit number | 2. Search by service detail ")
        if user_choice == "1":
            search_allox()
            break
        elif user_choice == "2":
            search_service()
            break
        else:
            print("Invalid Input, please try again")
            pass

def search_again():
    while True:
        user_choice = input("1. Query this database again | 2. Change Database | 3. Back to Menu ")
        if user_choice == "1":
            search()
            break
        elif user_choice == "2":
            db()
        elif user_choice == "3":
            main()
        else:
            print("Invalid Input, please try again")
            pass



main()