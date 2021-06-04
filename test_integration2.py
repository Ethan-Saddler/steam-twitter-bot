'''
This program uses code to tweet about game sales on Steam using data scraped from the Steam Scraper program built by 
Ethan. It requires the package tweepy and a Twitter developer account, which you must install using the command pip3 install tweepy.

This version is using the updated way we stored data (putting a special key between each necessary piece like title, org price,
discounted price, etc.)

To use this app under your own developer account, fill in your API Key, API Key Secret, Access Token, and Access Token Secret
where it is denoted. THey are found in lines 18-21.

Version 2
Name: Austin Zhuang
Date: 5/4/21
'''
import tweepy
import os

api_key = 
api_key_secret = 
access_token = 
access_token_secret = 

#Authenticate to Twitt
auth = tweepy.OAuthHandler(api_key,
api_key_secret)
auth.set_access_token(access_token,
access_token_secret)

#Create API object
api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)
key = '~@#!'

#file path to game sales document
base_path = os.path.join(os.path.dirname(__file__), "games_sales.txt")
tweets = []


#splicing each line in a file to get the necessary information and format it into a readable tweet
with open(base_path, encoding = "utf-8") as s:
    for line in s:
        if line != '\n' and "Free" not in line:
            game_attrs = line.split('~@#!')
            if int(game_attrs[3].strip('-%')) >= 30 and float(game_attrs[1].strip('$')) > 1:
                tweets.append(game_attrs[0] + " is on sale now for " + game_attrs[2] + 
                " from a original price of " + game_attrs[1] + ", a " + game_attrs[3].strip('-') + " discount " + game_attrs[4])
api.update_status(tweets[0])