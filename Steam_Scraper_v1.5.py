'''
This program requires anaconda (an alterante version of python) and both selenium and beautifulsoup (used for webscraping and control)
currently the program is able to launch a tab of chrome which also requires chromedriver to be installed (edit path of chromedriver under 
"webdriver.Chrome(executable_path=r"insert here")). It then scrolls to the bottom of the page to load the full html content then 
reads it, saves it then parses it. Finally it currently only finds the discount saves it to a list. However, the plan is to store the 
name and price.

Version: v1
Name: Ethan Saddler

'''



#modules
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import bs4

from urllib.request import urlopen as req
from bs4 import BeautifulSoup as soup

#essentially removes tags and unnecessary content (indents, new lines, etc.)
def Clean_content(content):
    n = 0
    for x in content:
        content[n] = x.text.strip()
        n += 1
    return content

def list_space(content):
    for i in content:
        print(i + "\n")

#identifying path of chromedriver
browser = webdriver.Chrome(executable_path=r"C:\Users\ehane\SP\chromedriver.exe")

#opening steam store
browser.get("https://store.steampowered.com/search/?category1=998&specials=1")
time.sleep(0.5)

#accessing the body of the site
element = browser.find_element_by_tag_name("body")

#500 overshoots as each pgdn goes about 11 games down. However; this accounts for loading times and variation in the amount of games.
#Can be reduced for testing
no_of_pagedowns = 500 
#while loop of paging down to reach bottom of site (overshoots to account for error)
while no_of_pagedowns:
    element.send_keys(Keys.PAGE_DOWN)
    time.sleep(0.2)
    no_of_pagedowns-=1

#sets the page source to a variable
steam_html = browser.page_source

#parsing html
steam_soup = soup(steam_html, "html.parser")

#stores all game containers
Game_Container = steam_soup.findAll("div", {"class":"responsive_search_name_combined"})

Discount_Percentage = []
Price = []
Name = []

#for loop to organize all of the data (Discount percent, Price (both original and new) and Name)
for container in Game_Container:
    Discount_Percentage.append(container.find("div", {"class":"col search_discount responsive_secondrow"}))
    Price.append(container.find("div", {"class":"col search_price discounted responsive_secondrow"}))
    Name.append(container.find("div", {"class":"col search_name ellipsis"}))



# Uncomment lines below to have the program print the lists of data

# print(Clean_content(Discount_Percentage))
# print(Clean_content(Price))
# print(Clean_content(Name))


# Uncomment to check that they have collected for the same amount of games (returns length of each list)

# print(len(Discount_Percentage))
# print(len(Price))
# print(len(Name))

# Uncomment to print a list of all games on sale 

list_space(Clean_content(Name))
