from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
import time

'''
Seasonal stats for every player in the NBA starting from 1991 to the end of the 2022 NBA regular season.
'''

# The years that we are interested in
seasons = list(range(1991, 2023))


per_game_url = "https://www.basketball-reference.com/leagues/NBA_{}_per_game.html"

# had to increment this variable manually since Safari only allows one remote session at a time, and
# I did not want to download an unsecure chromedriver.
season = 2022

url = per_game_url.format(season)

driver = webdriver.Safari(executable_path="/usr/bin/safaridriver")
driver.get(url)
driver.execute_script("window.scrollTo(1, 10000)")
time.sleep(2)

html = driver.page_source

with open("player_stats/{}".format(season), "w+") as y:
    y.write(html)
dfs = []
for season in seasons:
    with open("player_stats/{}".format(season)) as f:
        page = f.read()
    soup = BeautifulSoup(page, "html.parser")
    soup.find('tr', class_="thead").decompose()
    player_table = soup.find(id="per_game_stats")
    player = pd.read_html(str(player_table))[0]
    player["Year"] = season
    dfs.append(player)

players = pd.concat(dfs)
players.to_csv('players.csv')
