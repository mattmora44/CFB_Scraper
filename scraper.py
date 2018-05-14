from bs4 import BeautifulSoup
import requests
import lxml
import os, os.path, csv

# this is a script that pulls information on players that were rated
# in ESPN College Football's prospect list on the user's specified year.

#take input
year = 0;
while (year > 2019 or year < 2006):
    year = int(input("Enter Year to pull top football prospects: "))

# ask if user wants to include non rated players

dontInclude = False
ans = 'empty'
while (ans != 'y' and ans != 'n' and ans != 'Y' and ans != 'N' and ans != 'yes' and ans != 'no' and ans != 'YES' and ans != 'NO'):
    userIn = str(input("Would you like to include players with no ratings? (y/n): "))
    ans = userIn
if (ans == 'y' or ans == 'Y' or ans == 'yes' or ans == 'YES'):
    print("Players with ratings will be included.")
    dontInclude = False
else:
    print("Players with ratings will not be included.")
    dontInclude = True

# initializing the url to a string
listingurl = "http://www.espn.com/college-sports/football/recruiting/databaseresults/_/sportid/24/class/" + str(year) +"/sort/school/starsfilter/GT/ratingfilter/GT/statuscommit/Commitments/statusuncommit/Uncommited"
url2 = "http://www.espn.com/college-sports/football/recruiting/databaseresults/_/page/2/sportid/24/class/2009/sort/school/starsfilter/GT/ratingfilter/GT/statuscommit/Commitments/statusuncommit/Uncommited"

# parse the url
response = requests.get(listingurl)
soup = BeautifulSoup(response.text, "lxml")
# soup contains all the html from the page

listings = [] # final list that holds all the information

# Find number of pages
numPages = soup.find("div", class_="page-numbers").get_text()
temp = numPages[5:]
n = int(temp)
print("Number of Pages: "+ str(n))

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
        hometown = rows.find_all("td")[1].get_text()
        school = hometown[hometown.find(",")+4:]
        city = hometown[:hometown.find(",")+4]
        position = rows.find_all("td")[2].get_text()
        grade = rows.find_all("td")[4].get_text()
        if (dontInclude == True):
            if (grade != "NR" and grade != "POST"):
                listings.append([name, school, city, position, grade])
        else:
            listings.append([name, school, city, position, grade])
print("Fetched page 1 of "+ str(n))

for i in range(2,n):
    # traversing through all the pages
    newURL = listingurl[:72] + '/page/' + str(i) + listingurl[72:]
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
            hometown = rows.find_all("td")[1].get_text()
            school = hometown[hometown.find(",")+4:]
            city = hometown[:hometown.find(",")+4]
            position = rows.find_all("td")[2].get_text()
            grade = rows.find_all("td")[4].get_text()
            if (dontInclude == True):
                if (grade != "NR" and grade != "POST"):
                    listings.append([name, school, city, position, grade])
            else:
                listings.append([name, school, city, position, grade])

    print("Fetched page " + str(i)+" of "+str(n))
# done with fetching, outputting to filename

filename = str(year) + "FB_Prospects"
with open(filename + ".csv", 'w', encoding='utf-8') as toWrite:
    writer = csv.writer(toWrite)
    writer.writerows(listings)
print(" ")
print("ESPN College Football listings fetched for the year "+ str(year) + ".")
