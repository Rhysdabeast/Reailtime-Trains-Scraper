# Realtime-Trains-Scraper
A very simple scraper for https://www.realtimetrains.co.uk/ which exports to a local database file!

# Packages
Packages you need in order to run the program: <br />
Requests - https://pypi.org/project/requests/ <br />
Beautifulsoup4 - https://pypi.org/project/beautifulsoup4/ <br />
Pandas - https://pypi.org/project/pandas/ <br />
openpyxl - https://pypi.org/project/openpyxl/ <br />

# Running the Program
First of all clone this repository or download it in ZIP format. 
From the project folder you can open the command prompt and type: <br />
<code>python RTT_Scraper_Main.py</code> <br />
<br />
![RTT CMD Example](https://user-images.githubusercontent.com/86208560/159197557-c8fec7dd-f97f-4284-af71-f4675ae91545.gif)<br />

Or you can open the project folder in Visual Studio Code or your prefered IDE and run the program through that:<br />
https://code.visualstudio.com/

# Using the Program

The program is very simple to use, when you get the program running it will ask for a station name which you would like to scrape services from. To make sure you enter the correct name look inside the excel spreadsheet and copy the station name from that if necessary. This would be useful if you wanted to get services from Acton Bridge for example, if Acton Bridge was inputted a database file would be created but with no data inside of it. Instead you would have to input Acton Bridge (Cheshire) as that is what corresponds to the correct CRS code for Acton Bridge. <br />

When a valid station name is inputted the program will run through and get the service details and allocation if available from every service at that given location. This is then exported to a database file.<br />
Details about allocations and which TOC's support this can be found here: https://www.realtimetrains.co.uk/about/knowyourtrain/

# Viewing the results
After the program finishes the results can be found in the database file it creates for the corresponding station you entered. These can be found in the <code>Databases</code> folder within the project folder. The file should be called <code>The Station Name you inputted.db</code><br />
To view the data you can use DB Browser for SQLite which is free to download from https://sqlitebrowser.org/dl/. <br />
Inside the database it should create a table called <code>The Station Name you inputted_Year_Month_Day</code>. In the table it will list all the services and allocations at that Station on that particular date. 
