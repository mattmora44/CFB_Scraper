from bs4 import BeautifulSoup
import requests
import lxml
import os, os.path, csv

# initializing the url to a string
listingurl = "http://www.espn.com/college-sports/football/recruiting/databaseresults/_/sportid/24/class/2009/sort/school/starsfilter/GT/ratingfilter/GT/statuscommit/Commitments/statusuncommit/Uncommited"
url2 = "http://www.espn.com/college-sports/football/recruiting/databaseresults/_/page/2/sportid/24/class/2009/sort/school/starsfilter/GT/ratingfilter/GT/statuscommit/Commitments/statusuncommit/Uncommited"

response = requests.get(listingurl)
soup = BeautifulSoup(response.text, "lxml")
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
        school = hometown[hometown.find(",")+4:]
        city = hometown[:hometown.find(",")+4]
        position = rows.find_all("td")[2].get_text()
        grade = rows.find_all("td")[4].get_text()
        if (grade != "NR" and grade != "POST"):
            listings.append([name, school, city, position, grade])

for i in range(2,257):
    newURL = listingurl[:72] + '/page/' + str(i) + listingurl[72:]
    #print(newURL)
    response = requests.get(newURL)
    soup = BeautifulSoup(response.text, "lxml")
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
            school = hometown[hometown.find(",")+4:]
            city = hometown[:hometown.find(",")+4]
            position = rows.find_all("td")[2].get_text()
            grade = rows.find_all("td")[4].get_text()
            if (grade != "NR" and grade != "POST"):
                listings.append([name, school, city, position, grade])

    print("Fetched page " + str(i))

with open("footballers2009.csv", 'w', encoding='utf-8') as toWrite:
    writer = csv.writer(toWrite)
    writer.writerows(listings)
print(" ")
print("ESPN College Football listings fetched.")
