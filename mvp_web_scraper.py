from bs4 import BeautifulSoup
import requests
import pandas as pd


# The years that we want the MVP's from
seasons = list(range(1991, 2023))

'''
Regular season MVP in the NBA starting from 1991 to the end of the 2022 NBA regular season.
'''

# the URL that we will use to extract information from
# we used curly brackets to be able to use formatted strings and get multiple years without having
# extract a URL for each year we want to predict the MVP for.
br_url = "https://www.basketball-reference.com/awards/awards_{}.html"


for season in seasons:
    url = br_url.format(season)
    data = requests.get(url)

    with open("mvp_stats/{}".format(season), "w+") as x:
        x.write(data.text)

dfs = []
for season in seasons:
    with open("mvp_stats/{}".format(season)) as f:
        page = f.read()
    soup = BeautifulSoup(page, "html.parser")
    soup.find('tr', class_="over_header").decompose()
    mvp_table = soup.find(id="mvp")
    mvp = pd.read_html(str(mvp_table))[0]
    mvp["Year"] = season
    dfs.append(mvp)

mvps = pd.concat(dfs)
mvps.to_csv("mvps.csv")
