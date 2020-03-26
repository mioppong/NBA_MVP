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
if(now.month >= 10):
    current_year = now.year +1
else:
    current_year = now.year
#---------GETTING THE CURRENT YEAR, IT CHANGES AS THE YEARS GO BY

df_players = pd.DataFrame()


#client.regular_season_player_box_scores(player_identifier="westbru01",season_end_year=2019,)

for x in client.players_advanced_season_totals(season_end_year=current_year):
    df_players = df_players.append(pd.DataFrame(x), ignore_index=True)

df_players = df_players.sort_values(by='win_shares', ascending=False, ignore_index=True).head(50)
df_players = df_players[['slug','name','win_shares']]
df_players['my_calc'] = ""
df_players['wins'] = 0

for index, player in df_players.iterrows():
    player_stats = pd.DataFrame(client.regular_season_player_box_scores(player_identifier=player['slug'],season_end_year=current_year))
    counter = 0
    for x in player_stats['outcome']:
        if (x.value) == 'WIN':
            counter += 1
    df_players.loc[index,'wins'] = counter
    df_players.loc[index,'my_calc'] = round(player['win_shares']/counter,2)
        

#---------- HERE I REMVOE PLAYERS NOT WITHIN MY VALUE OF 0.2 TO 0.35
df_players = df_players[df_players.my_calc > 0.20]
df_players = df_players[df_players.my_calc < 0.35]


with open("prediction.txt", 'w+') as f:
    for index,player in df_players.iterrows():
        f.write(player['name']+ '\n')

#print(df_players)
