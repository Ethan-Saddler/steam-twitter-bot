'''

Reqs: This program requires anaconda and both selenium and beautifulsoup (used for webscraping and control)
currently the program is able to launch a tab of chrome which also requires chromedriver to be installed (edit path of chromedriver under 
"webdriver.Chrome(executable_path=r"insert here")). Zip comes with every other file needed, but if not you need games_new.txt,
games_old.txt and games_sales.txt. This program is meant to be used in conjunction with something that formats the text files,
as the content is seperated by a key. Run through changing directory to where file is stored

Features: It opens a window, then scrolls down to load the full page. Then it downloads the html, closes the window and parses.
Finally it searches for the required tags and saves them in a list then. Saves all games (new/old) to a txt file then cross references 
to find new games on sale.

Contributions: See line 153-157, Austin Zhuang helped build for loop for links, and helped adapt it to main.

Version: Master - Stores games locally to cross reference and store txt file of games on sale. Used in conjunction with twitter bot.
Name: Ethan Saddler

'''


#modules

import time

import re

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

import bs4

from urllib.request import urlopen as req
from bs4 import BeautifulSoup as soup

import os
import pathlib


# file paths
basepath = pathlib.Path(__file__).parent.absolute()

# path variables

games_new_path = os.path.join(basepath, "games_new.txt")
games_old_path = os.path.join(basepath, "games_old.txt")
games_sales_path = os.path.join(basepath, "games_sales.txt")
chrome_driver_path = os.path.join(basepath, "chromedriver.exe")

#this variable is used to separate the necessary data for each game
key = '~@#!'


#functions

#removes tags and unnecessary content (indents, new lines, etc.)
def clean_content(content):
    n = 0
    for x in content:
        content[n] = x.text.strip()
        n += 1
    return content

#formats name, price and percentage into a line
def organize_game_info(game, prices, percentage, link):
    index = 0
    game_entry = []
    for x in game:
        game_entry.append(x + prices[index] + key + percentage[index] + key + link[index] + "\n\n")
        index+=1
    strg = ""
    game_entry = strg.join(game_entry)
    return game_entry
    

'''                         main                        '''


# Setting up files for program: new becomes old and clears new
# (Path of the file to be opened, how to open it - read or write, what encoding to open with)
games_new = open(games_new_path,"r", encoding="utf-8")
games_old = open(games_old_path,"w+", encoding="utf-8")
for line in games_new:
    games_old.write(line)
games_new = open(games_new_path,"w+", encoding="utf-8")
games_old.close()

# identifying path of chromedriver
browser = webdriver.Chrome(executable_path=chrome_driver_path)

# opening steam store
browser.get("https://store.steampowered.com/search/?sort_by=Name_ASC&category1=998&supportedlang=english&specials=1")
time.sleep(0.5)

# reading source to determine how many games there are on the page
steam_html = browser.page_source

# parsing the raw page source
steam_soup = soup(steam_html, "html.parser")

# determining num of pgdn's needed

# finding the text at top of page that contains the number of games
game_num = steam_soup.find("div", {"id":"search_results_filtered_warning_persistent"})
text_game_num = game_num.div.text
string_game_num = str(text_game_num)

#removes the commas from the string, so that it can be an integer. .split seperates each word into strings on a list.
int_game_num = int(string_game_num.split()[0].replace(",", ""))

no_of_pagedowns = int_game_num//10

#accessing the body of the site so that you can interact with it
element = browser.find_element_by_tag_name("body")

#while loop of paging down to reach bottom of site (overshoots to account for error)
while no_of_pagedowns:
    # enters keys on "body" of page.
    element.send_keys(Keys.PAGE_DOWN)
    time.sleep(0.3)
    no_of_pagedowns-=1

print("\n\n\n\n\n\nweb scrape complete...")

#sets the page source to a variable
steam_html = browser.page_source

#closes chrome window
browser.close()

#parsing html
steam_soup = soup(steam_html, "html.parser")

#stores all game containers
game_container = steam_soup.findAll("div", {"class":"responsive_search_name_combined"})
search_row = steam_soup.find("div", {"id":"search_resultsRows"})
game_links = search_row.findAll("a")
links_to_pages = []
discount_percentage = []
price = []
new_name = []


#for loop to organize all of the data (discount percent, price (both original and new) and name)
for container in game_container:
    # checks to see if the game is a "special", but not on sale.
    if container.find("div", {"class":"col search_price discounted responsive_secondrow"}) != None:
        discount_percentage.append(container.find("div", {"class":"col search_discount responsive_secondrow"}))
        price.append(container.find("div", {"class":"col search_price discounted responsive_secondrow"}))
        new_name.append(container.find("div", {"class":"col search_name ellipsis"}))
        

for link in game_links:
    if link.find("div", {"class":"col search_price discounted responsive_secondrow"}) != None:
        # searching for attribute "href" and if it starts with url
        if 'https://store.steampowered.com' in link.attrs['href']:
            links_to_pages.append(link.attrs['href'])

# removing tags and extra spaces
discount_percentage = clean_content(discount_percentage)
price = clean_content(price)
new_name = clean_content(new_name)

#properly formats the prices and names so that it has the keys seperating them
for n, x in enumerate(price):
    price[n] = x.replace("$", key + "$")

# removes VR Supported and VR Only from game content (for whatever reason it is stored with the title)
for n, x in enumerate(new_name):
    new_name[n] = x.replace("\n\nVR Only", "").replace("\n\nVR Supported", "")
    
# getting new games into games_new text file
game_text = ""
game_text = organize_game_info(new_name, price, discount_percentage, links_to_pages)

games_new.write(game_text)
games_new.close()

# re-opening files properly
games_new = open(games_new_path,"r", encoding="utf-8")
games_old = open(games_old_path,"r", encoding="utf-8")
games_sales = open(games_sales_path,"w+", encoding="utf-8")

# compiles text files into list to compare easier
games_new_list = []
for a in games_new:
    games_new_list.append(a)

games_old_list = []
for a in games_old:
    games_old_list.append(a)

games_sales_len = 0

# checking old and new games to find new sales
for line in games_new_list:
    if line not in games_old_list:
        games_sales.write(line)
        games_sales_len += 1

games_sales.close()
games_new.close()
games_old.close()

print("\n\n\n\n\n\n\n\n\nComplete :)\n\nThere were {} new sales.\n".format(games_sales_len))
