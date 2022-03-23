# Realtime-Trains-Scraper
A very simple scraper for https://www.realtimetrains.co.uk/ which exports to a local database file!

# Packages
Packages you need in order to run the program: <br />
Requests - https://pypi.org/project/requests/ <br />
Beautifulsoup4 - https://pypi.org/project/beautifulsoup4/ <br />
Pandas - https://pypi.org/project/pandas/ <br />
openpyxl - https://pypi.org/project/openpyxl/ <br />
tqdm - https://pypi.org/project/tqdm/

# Running the Program
First of all clone this repository or download it in ZIP format. 
From the project folder you can open the command prompt for Windows or Terminal for Mac and type: <br />
<code>python RTT_Scraper_Main.py</code> <br />
<br />
![RTT CMD Example](https://user-images.githubusercontent.com/86208560/159614577-6d82d846-1c9e-40d5-ae91-c731959f882c.gif)<br />

Or you can open the project folder in Visual Studio Code or your prefered IDE and run the program through that:<br />
https://code.visualstudio.com/

# Using the Program

The program is very simple to use, when you get the program running it will ask for you to enter either 1 or 2. 1 will ask you for a station name which you would like to scrape services from. 2 will exit the program. To make sure you enter the correct name look inside the excel spreadsheet and copy the station name from that if necessary. This would be useful if you wanted to get services from Acton Bridge for example, if Acton Bridge was inputted a database file would be created but with no data inside of it. Instead you would have to input Acton Bridge (Cheshire) as that is what corresponds to the correct CRS code for Acton Bridge. <br />

When a valid station name is inputted the program will run through and get the service details and allocation if available from every service at that given location. This is then exported to a database file.<br />
Details about allocations and which TOC's support this can be found here: https://www.realtimetrains.co.uk/about/knowyourtrain/<br >
<br />
![RTT CMD Example Full](https://user-images.githubusercontent.com/86208560/159616003-62f3d69a-2e39-4c1d-947d-ce40d05e9c6c.gif)


# Viewing the results
After the program finishes the results can be found in the database file it creates for the corresponding station you entered. These can be found in the <code>Databases</code> folder within the project folder. The file should be called <code>The Station Name you inputted.db</code><br />
To view the data you can use DB Browser for SQLite which is free to download from https://sqlitebrowser.org/dl/. <br />
Inside the database it should create a table called <code>The Station Name you inputted_Year_Month_Day</code>. In the table it will list all the services and allocations at that Station on that particular date.
<br />
<code>Example Database Structure:</code> <br />
<br />
![image](https://user-images.githubusercontent.com/86208560/159616146-80a93cf2-1f3d-48e3-a96e-d91882dd5f28.png) <br />
<br />
<code>Example Data:</code> <br />
</br>
![image](https://user-images.githubusercontent.com/86208560/159616377-9ba94b7e-c5aa-4d0b-8b26-1b246f4fa920.png)
