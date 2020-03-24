
import requests
from bs4 import BeautifulSoup
import pandas as pd
from pprint import pprint
import numpy as np
from basketball_reference_web_scraper import client
import datetime
import matplotlib.pyplot as plt


df_season = pd.DataFrame()
for x in (client.players_advanced_season_totals(season_end_year=2020)):
    df_season = df_season.append(pd.DataFrame(x), ignore_index=True)

df_season = df_season.head(10)
df_season['Wins'] = ""

df_regular_players = pd.DataFrame()
df_regular_players['name'] = ""
df_regular_players['slug'] = ""
df_regular_players['wins'] = ""
df_regular_players['WS'] = ""

for x,player in df_season.iterrows():
    win_counter = 0
    df_temp = pd.DataFrame(client.regular_season_player_box_scores(player_identifier=player['slug'],season_end_year=2020))

    for index, outcome in df_temp.iterrows():
        if (outcome['outcome'].value) == "WIN":
            win_counter = win_counter +1
    
    df_regular_players = df_regular_players.append({'name':player['name'],'slug':player['slug'],'wins':win_counter, 'WS':player['win_shares']},ignore_index=True)
  




print(df_regular_players)