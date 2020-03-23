import requests
from bs4 import BeautifulSoup
import pandas as pd
from pprint import pprint
import numpy as np
from basketball_reference_web_scraper import client
import datetime

#--------------SCRAPING THE LIST OF ALLSTARS FROM LINK BELOW--------------#--------------#--------------
URL = 'https://www.basketball-reference.com/awards/mvp.html'
response = requests.get(URL)
soup = BeautifulSoup(response.content, 'html.parser')

columns = ['Season','Lg','Player','Voting','Age','Tm','G','MP','PTS','TRB','AST','STL','BLK','FG%','3P%','FT%','WS','aa']
df = pd.DataFrame(columns=columns)
df2 = pd.DataFrame()

now = datetime.datetime.now()
current_year = now.year


table = soup.find('table', attrs={'id':'mvp_NBA','class':'sortable'}).tbody
trs = table.find_all('tr')

for tr in trs:
    tds = tr.find_all(['th','td'])
    row = [td.text.replace('\n', '') for td in tds]
    df = df.append(pd.Series(row,index=columns), ignore_index=True)

df = df.head(10)
df = df[['Season', 'Player','WS']]
df['id'] = ""
df['Wins'] = ""

#--------------ADDING THE ID OF EACH PLAYER TO THE DATAFRAME#--------------

#--------------GETTING ALL NBA PLAYERS OF THE CURRENT SEASON, 
#--------------GETTING THEIR ID, AND ADDING IT TO THE DATA FRAME OF MVPS
for x in (client.players_season_totals(season_end_year=current_year)):
    df2 = df2.append(pd.DataFrame(x), ignore_index=True)

for df_index, df_player in df.iterrows():
    for df2_index, df2_player in df2.iterrows():
        if df_player['Player'] == df2_player['name']:
             df_player['id'] = df2_player['slug']

for x in (client.players_season_totals(season_end_year=current_year-1)):
    df2 = df2.append(pd.DataFrame(x), ignore_index=True)

for df_index, df_player in df.iterrows():
    for df2_index, df2_player in df2.iterrows():
        if df_player['Player'] == df2_player['name']:
             df_player['id'] = df2_player['slug']
  
##--------------GETTING THE NUMBER OF WINS FOR EACH PLAYER FOR THEIR RESPECTIVE SEASOSN

for index, player in df.iterrows():
    year_mvp = player['Season'][:4]
    year_mvp = int(year_mvp) +1
    win_counter = 0

    df_temp = pd.DataFrame(client.regular_season_player_box_scores(player_identifier=player['id'], season_end_year=(year_mvp)))
    
    for index2, player2 in df_temp.iterrows():
        if player2['outcome'].value == 'WIN':
            win_counter = win_counter + 1

    print(player['Player'], ' supposed to have win ->', win_counter)
    player['Wins'] = win_counter

print(df)