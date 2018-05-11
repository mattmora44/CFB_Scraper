from bs4 import BeautifulSoup
import requests
import os, os.path, csv

# initializing the url to a string
listingurl = "http://www.espn.com/college-sports/football/recruiting/databaseresults/_/sportid/24/class/2016/sort/school/starsfilter/GT/ratingfilter/GT/statuscommit/Commitments/statusuncommit/Uncommited"

response = requests.get(listingurl)
soup = BeautifulSoup(response.text, "html.parser")
# soup contains all the html from the page
#print(soup.prettify())
listings = []
# <tr class="evenrow player-####">
# highlights the whole row
for rows in soup.find_all("tr"):
    # oddrow and evenrow are the names of the 2 types of rows
    # that we are copying
    if ("oddrow" in rows["class"]) or ("evenrow" in rows["class"]):
        #<div class="name">
        #   <a href= "http:...">
        #      <strong>Firstname Lastname</strong>
        name = rows.find("div", class_="name").a.get_text()
        #
        hometown = rows.find_all("td")[1].get_text()
print(hometown)
