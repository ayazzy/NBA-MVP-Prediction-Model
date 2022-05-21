from bs4 import BeautifulSoup
import requests
import pandas as pd

'''
Conference rankings for every team in the NBA starting from 1991 to the end of the 2022 NBA regular season.
'''

# The years that we are interested in
seasons = list(range(1991, 2023))

team_stats_url = "https://www.basketball-reference.com/leagues/NBA_{}.html"

for season in seasons:
    url = team_stats_url.format(season)
    data = requests.get(url)

    with open("team_stats/{}".format(season), "w+") as x:
        x.write(data.text)

dfs = []
for season in seasons:
    with open("team_stats/{}".format(season)) as f:
        page = f.read()

    soup = BeautifulSoup(page, "html.parser")
    soup.find('tr', class_="thead").decompose()
    team_table = soup.find(id="divs_standings_E")
    team = pd.read_html(str(team_table))[0]
    team["Year"] = season
    team["Team"] = team["Eastern Conference"]
    del team["Eastern Conference"]
    dfs.append(team)

    soup = BeautifulSoup(page, "html.parser")
    soup.find('tr', class_="thead").decompose()
    team_table = soup.find(id="divs_standings_W")
    team = pd.read_html(str(team_table))[0]
    team["Year"] = season
    team["Team"] = team["Western Conference"]
    del team["Western Conference"]
    dfs.append(team)

teams = pd.concat(dfs)
teams.to_csv("teams.csv")
