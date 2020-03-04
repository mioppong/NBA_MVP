import csv
import sys
import pandas as pd
import numpy as np
from collections import defaultdict
import argparse
from pprint import pprint
import operator
import matplotlib.pyplot as plt
import math
from pprint import pprint

def main():
    nba_teams = {
        "MIL":"Milwaukee Bucks",
        "TOR":"Toronto Raptors",
        "GSW":"Golden State Warriors",
        "DEN":"Denver Nuggets",
        "HOU":"Houston Rockets",
        "POR":"Portland Trail Blazers",
        "PHI":"Philadelphia 76ers",
        "UTA":"Utah Jazz",
        "BOS":"Boston Celtics",
        "OKC":"Oklahoma City Thunder",
        "IND":"Indiana Pacers",
        "LAC":"Los Angeles Clippers",
        "BRK":"Brooklyn Nets",
        "SAS":"San Antonio Spurs",
        "ORL":"Orlando Magic",
        "DET":"Detroit Pistons",
        "CHO":"Charlotte Hornets",
        "MIA":"Miami Heat",
        "SAC":"Sacramento Kings",
        "LAL":"Los Angeles Lakers",
        "MIN":"Minnesota Timberwolves",
        "DAL":"Dallas Mavericks",
        "MEM":"Memphis Grizzlies",
        "NOP":"New Orleans Pelicans",
        "WAS":"Washington Wizards",
        "ATL":"Atlanta Hawks",
        "CHI":"Chicago Bulls",
        "CLE":"Cleveland Cavaliers",
        "PHO":"Phoenix Suns",
        "NYK":"New York Knicks"
    }

    #----------arguments#----------------------------------------
    parser = argparse.ArgumentParser()
    parser.add_argument("allstar_team1", help="1st team in all stars")
    parser.add_argument("allstar_team2", help="2nd team in all stars")
    parser.add_argument("currteamstats", help="current teamstats")
    parser.add_argument("currplayerstats",help="current playerstats")

    #this gets the arguments and saves them to a 
    #certain variable
    args = parser.parse_args()
    allstar_team1 = args.allstar_team1
    allstar_team2 = args.allstar_team2
    currteamstats = args.currteamstats
    currplayerstats = args.currplayerstats

    #----------this reads files into a dataframe
    df_allstar_team1 = pd.read_csv(allstar_team1)
    df_allstar_team2 = pd.read_csv(allstar_team2)
    df_teams = pd.read_csv(currteamstats)    
    df_players = pd.read_csv(currplayerstats)

    #----------This section gets the top players with highest win shares and adds them to the allstars list
    #----------Just in case they blow up in the current season
    blew_up = df_players.sort_values('WS', ascending=False).head(10)
    blew_up_players = blew_up[['Player','Tm']]
    for index,player in blew_up_players.iterrows():
        if (player['Player'] in df_allstar_team1['Starters'].values or (player['Player'] in df_allstar_team2['Starters'].values) ):
            blew_up_players = blew_up_players.drop([index])
    
    blew_up_players = blew_up_players.rename(columns={'Player':'Starters'})
    df_allstar_team1 = df_allstar_team1.append(blew_up_players,sort=True)
    

    prediction_dict = {}
    #----------For each allstar
    for index, allstar in df_allstar_team1.iterrows():
        name = allstar['Starters']
        team = nba_teams[allstar['Tm']]

        player_row = df_players.loc[df_players['Player'] == name,['WS']]
        win_shares = 0.0
        if (not (player_row.empty)):
            win_shares = round(float(player_row.values),2)
                    
        team_row = df_teams.loc[df_teams['Team'] == team]
        row,random_a, random_b = (team_row['Overall'].to_string()).partition('-')
        
        #WE CANT CHAGE THIS BECAUSE THE CSV FILES DOES THIS IDK WHY
        #4 EXACT SPACES
        wins = row.split('   ')[1]
        div = round(win_shares / int(wins),2)
        prediction_dict[name] = div
        #print(name+'\t'+ str(div))

    for index, allstar in df_allstar_team2.iterrows():
        name = allstar['Starters']
        team = nba_teams[allstar['Tm']]

        player_row = df_players.loc[df_players['Player'] == name,['WS']]
        win_shares = 0.0
        if (not (player_row.empty)):
            win_shares = round(float(player_row.values),2)
                    
        team_row = df_teams.loc[df_teams['Team'] == team]
        row,random_a, random_b = (team_row['Overall'].to_string()).partition('-')
        
        #WE CANT CHAGE THIS BECAUSE THE CSV FILES DOES THIS IDK WHY
        #4 EXACT SPACES
        wins = row.split('   ')[1]
        div = round(win_shares / int(wins),6)
        prediction_dict[name] = div
        #print(name+'\t'+ str(div))
    #pprint(sorted(prediction_dict.items(), key=lambda x: 0.25))
    #pprint(prediction_dict)

    for k in list(prediction_dict):
        if(prediction_dict[k] < 0.2 or prediction_dict[k] > 0.35):
            prediction_dict.pop(k,None)
    
    with open("prediction.txt", 'w+') as f:
        for k,v in prediction_dict.items():
            f.write(k + '\t' + str(v)+ '\n')
            
if __name__=="__main__":
    main()