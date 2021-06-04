# Steam Scraper
Steam Scraper opens a window, then scrolls down to load the full page. It downloads the html, closes the window and parses. It searches for the required tags and saves them in a list then. Saves all games (new/old) to a txt file then cross references to find new games on sale. Includies game name, og price, new price, percentage and link to game.

# Requirements
Python -- Only extra libraries needed are bs4 (HTML Parser) and selenium (webdriver)  
  
To install, cd into the file's folder and do "pip install -r requirements.txt"   
  
Also requires [chromedriver](https://chromedriver.chromium.org/downloads) - be sure to place chromedriver.exe in the same folder as Steam_Scraper.py

# Usage

## Windows
Unzip Steam_Scraper_Main.zip and put all the contents in the same folder (with chromedriver.exe). Then simply run the executable (may require administrator). The first time, every game scraped should return in game_sales.txt; however, if you run it again, it will return an accurate update of new games on sale, albeit with them seperated by a key, which is used to split the lines later when formatting an alert outside the text file.  

## Mac
Unzip Steam_Scraper_Main.zip and put all the contents in the same folder (with chromedriver.exe). Open terminal and type "cd Steam_Scraper_Main". Then type "python ./Steam_Scraper_Master.py". The first time, every game scraped should return in game_sales.txt; however, if you run it again, it will return an accurate update of new games on sale, albeit with them seperated by a key, which is used to split the lines later when formatting an alert outside the text file.  



