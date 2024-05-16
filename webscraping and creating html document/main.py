"""
Student name: Ujwal Timisena Chhetri ,
Student ID: 200567407,
Email: uzalxettri10@gmail.com,
Last Modified Date: 2024-03-19 08:36 PM
"""

import requests
import os
import re
from os.path import basename
from bs4 import BeautifulSoup
 #step 1 i send get request to url and stores the response
# URL of the website
url = "https://www.ourcommons.ca/Members/en/search"
res = requests.get(url) #sending GET request to the url and storing the response
# prasing the html content of the response using BeautifulSoup
soup = BeautifulSoup(res.text, "lxml")
# finding all the div elements with the specified class
_all = soup.find_all("div", attrs={"class":"col-lg-4 col-md-6 col-xs-12"})

maleUrl = "https://www.ourcommons.ca/members/en/search?caucusId=all&province=all&gender=M"  # url for male
resMale = requests.get(maleUrl)  # sending GET request to the maleurl
soupMale = BeautifulSoup(resMale.text, "lxml")  # prasing the html content of the response using BeautifulSoup

femaleUrl = "https://www.ourcommons.ca/members/en/search?caucusId=all&province=all&gender=F"  # url for female
resFemale = requests.get(femaleUrl)  # sending GET request to the femaleurl
soupFemale = BeautifulSoup(resFemale.text, "lxml")  # prasing the html content of the response using BeautifulSoup

#step2 i created function for getting male and female members name to get gender
#creating function to get the name of male and females members
def forgettingmembersgender():
    # Extracting all names of male members
    maleMembersNames = [div.find("div", attrs={"class": "ce-mip-mp-name"}).get_text() for div in
                        soupMale.find_all("div", attrs={"class": "col-lg-4 col-md-6 col-xs-12"})]
    # Extracting all names of female members
    femaleMembersnames = [div.find("div", attrs={"class": "ce-mip-mp-name"}).get_text() for div in
                          soupFemale.find_all("div", attrs={"class": "col-lg-4 col-md-6 col-xs-12"})]

    return maleMembersNames, femaleMembersnames #return list of male and female name

#step3
# i created function for getting members details like name, link, gender, image, party, province, constituency

def gettingmembersdata():
    # making empty list to store member data
    members = []
    #getting name of male and females member
    maleMembersNames, femaleMembersnames = forgettingmembersgender()
    # looping each div element found
    for k, div in enumerate(_all, start=1):
        # finding div element containing the member's name
        Name = div.find("div", attrs={"class": "ce-mip-mp-name"})
        # printing members name
        print(Name.get_text())
        # Checking if the name is in the list of male or female members
        if Name.get_text() in maleMembersNames:
            gender = "Male"
        else:
            gender = "Female"
        print(gender) #printing gender

        # finding div element containing the member's Party
        Party = div.find("div", attrs={"class": "ce-mip-mp-party"})
        print(Party.get_text()) #printing party

        # finding div element containing the member's Province
        Province = div.find("div", attrs={"class": "ce-mip-mp-province"})
        print(Province.get_text()) #printing province

        # finding div element containing the member's Constituency
        Constituency = div.find("div", attrs={"class": "ce-mip-mp-constituency"})
        print(Constituency.get_text()) #printing Constituency

        # finding a element containing the member's link
        Link = div.find("a", attrs={"class": "ce-mip-mp-tile"}, href=True)
        Link = Link['href']  # extracting href attributes
        # Constructing the full URL using the extracted 'href' value
        Link_ = f"http://www.ourcommons.ca{Link}"
        # printing the constructed full image url
        print(Link_)
        # finding img element containing the member's Image
        Img = div.find("img", attrs={"class": "ce-mip-mp-picture visible-lg visible-md img-fluid"})
        # extracting the src
        Img = Img['src']
        # Constructing the full image URL using the extracted 'src' value
        Imgurl = "http://www.ourcommons.ca" + Img
        # prints image url
        print(Imgurl)
        # Extracting the base filename from the Imgurl variabl
        filename = basename(Imgurl)
        # Constructing  full path to save image file using the current working directory and  filename
        Imgpath = os.path.join(os.getcwd(), filename)
        # saving the image content
        with open(Imgpath, 'wb') as f:
            f.write(requests.get(Imgurl).content)

        # Append member data as a dictionary to the members
        members.append({
            "Name": Name,
            "Gender": gender,
            "Party": Party,
            "Province": Province,
            "Constituency": Constituency,
            "Link_": Link_,
            "Image": Imgurl

        })
    return members #returning list of member data


# step 4 i created function to create html table
def creatinghtmltable(members):
    #constructing table using html elements
    htmltable = "<html><head><title>Members</title></head><body>"
    htmltable += "<table border='1'><tr><th>Sr. No</th><th>Name</th><th>Gender</th><th>Party</th><th>Province</th><th>Constituency</th><th>Link</th><th>Image</th></tr>"
    #using loop  to generate row for each member
    for i, member in enumerate(members, start=1):
        #adding row
        htmltable += (f"<tr><td>{i}</td>"
                      f"<td><b>{member['Name']}</b></td>"
                      f"<td>{member['Gender']}</td>"
                      f"<td>{member['Party']}</td>"
                      f"<td>{member['Province']}</td>"
                      f"<td>{member['Constituency']}</td>"
                      f"<td><a href='{member['Link_']}'>{member['Link_']}</a></td>"
                      f"<td><img src='{member['Image']}' alt='{member['Name']}'></td></tr>")
    #completing html structure
    htmltable += "</table></body></html>"
    #  writing the HTML content to a file named "commons.html"
    with open("commons.html", "w") as f:
        f.write(htmltable)
#step5 for  running script
if __name__ == "__main__": #for running script directly
    # Calling the function to get member genders
    maleMembersNames, femaleMembersnames = forgettingmembersgender()

    # Calling the function to get member data
    members = gettingmembersdata()

    # Creating HTML table using member data
    creatinghtmltable(members)











