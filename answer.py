import requests
from bs4 import BeautifulSoup
import pandas as pd
from pprint import pprint
import numpy as np
from basketball_reference_web_scraper import client
import datetime
import matplotlib.pyplot as plt

#---------GETTING THE CURRENT YEAR, IT CHANGES AS THE YEARS GO BY
now = datetime.datetime.now()
current_year = now.year
#---------GETTING THE CURRENT YEAR, IT CHANGES AS THE YEARS GO BY

df_players = pd.DataFrame()


#client.regular_season_player_box_scores(player_identifier="westbru01",season_end_year=2019,)

for x in client.players_advanced_season_totals(season_end_year=current_year):
    df_players = df_players.append(pd.DataFrame(x), ignore_index=True)

df_players = df_players[['slug','name','win_shares']]
df_players['my_calc'] = ""
df_players['wins']

for index, player in df_players.iterrows():
    DataFrame(client.regular_season_player_box_scores(player_identifier=player['slug'],season_end_year=current_year))
    
    player['wins']

print(df_players)
