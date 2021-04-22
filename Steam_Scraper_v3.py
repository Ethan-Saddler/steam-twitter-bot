'''

Reqs: This program requires anaconda and both selenium and beautifulsoup (used for webscraping and control)
currently the program is able to launch a tab of chrome which also requires chromedriver to be installed (edit path of chromedriver under 
"webdriver.Chrome(executable_path=r"insert here")). 

Features: Currently it opens a window, then scrolls down to load the full page. Then it downloads the html, closes the window and parses.
Finally it searches for the required tags and saves them in a list then.

Version: v3 - added chrome close and fixed description

Name: Ethan Saddler

'''

#modules

import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import bs4

from urllib.request import urlopen as req
from bs4 import BeautifulSoup as soup

#functions

#essentially removes tags and unnecessary content (indents, new lines, etc.)
def Clean_content(content):
    n = 0
    for x in content:
        content[n] = x.text.strip()
        n += 1
    return content

#prints list with spaces
def list_space(content):
    for i in content:
        print(i + "\n")

#identifying path of chromedriver
browser = webdriver.Chrome(executable_path=r"C:\Users\ehane\SP\chromedriver.exe")

'''                         main                        '''

#opening steam store
browser.get("https://store.steampowered.com/search/?category1=998&specials=1")
time.sleep(0.5)

#reading source to determine how many games
steam_html = browser.page_source
steam_soup = soup(steam_html, "html.parser")

#determining num of pgdn's needed
game_num = steam_soup.find("div", {"id":"search_results_filtered_warning_persistent"})
text_game_num = game_num.div.text
string_game_num = str(text_game_num)
int_game_num = int(string_game_num.split()[0].replace(",", ""))

no_of_pagedowns = int_game_num//10

#accessing the body of the site
element = browser.find_element_by_tag_name("body")

#while loop of paging down to reach bottom of site (overshoots to account for error)
while no_of_pagedowns:
    element.send_keys(Keys.PAGE_DOWN)
    time.sleep(0.2)
    no_of_pagedowns-=1

#sets the page source to a variable
steam_html = browser.page_source

#closes chrome window
browser.close()

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

'''                 debug                   '''

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
