import sqlite3

tn = []
station_name = input("Please enter a station name you would like to query: ")
con = sqlite3.connect("Databases/" + station_name + ".db")
cursor = con.cursor()

res = con.execute("SELECT name FROM sqlite_master WHERE type='table';")
for name in res.fetchall():
    tn.append(name[0])

tn.remove("sqlite_sequence")
print(tn)

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
        user_choice = input("1. Search again | 2. Exit ")
        if user_choice == "1":
            search()
            break
        elif user_choice == "2":
            exit()
            break
        else:
            print("Invalid Input, please try again")
            pass

search()