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


def main():
    #----------This section maps out nba team 
    #----------accronyms to the full name
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
   
    #----------This plots the difference b/w nba players and mvp's
    
    #----------we get prev nba mvp's
    #----------Then we pass any stats from any season
    #----------and include the teams stats from that season  team wins and losses
    parser = argparse.ArgumentParser()
    parser.add_argument("past_mvps", help="past mvps")
    parser.add_argument("all_players", help="nba season of all players")
    parser.add_argument("all_teams",help="nba teams of same year as all players")

    #----------this gets the arguments and saves them to a 
    #----------certain variable
    args = parser.parse_args()
    past_mvps = args.past_mvps
    all_players = args.all_players
    all_teams = args.all_teams
    
    #----------this reads files into a dataframe
    df_mvps = pd.read_csv(past_mvps)
    df_all_players = pd.read_csv(all_players)
    df_teams = pd.read_csv(all_teams)

    #----------We plot the past 10 nba season mvp's
    first_10 = df_mvps.head(10)
    x_vals = list(first_10['Player'])
    y_vals = []

    for index, star in first_10.iterrows():
        y_vals.append(round(star['WS']/star['TW'],2))

    plt.scatter(x_vals,y_vals, label="past 10 mvp's")
    
    #----------We basically calculate
    #----------win shares/total team wins, here
    #----------and append it to y_vals_all 
    x_vals_all = list(df_all_players['Player'])
    y_vals_all = []
    
    for index, player in df_all_players.iterrows():
        if player['Tm'] == 'TOT':
            df_all_players.drop(index,axis=0,inplace=True)


    for index, player in df_all_players.iterrows():
        name = player['Player']
        team = nba_teams[player['Tm']]

        player_row = df_all_players.loc[df_all_players['Player'] == name,['WS']]
        win_shares = 0.0
        if (not (player_row.empty)):
            print(name)
            win_shares = round(float(player_row.values),2)
                    
        team_row = df_teams.loc[df_teams['Team'] == team]
        row,random_a, random_b = (team_row['Overall'].to_string()).partition('-')
        
        #WE CANT CHAGE THIS BECAUSE THE CSV FILES DOES THIS IDK WHY
        #4 EXACT SPACES
        wins = row.split('   ')[1]
        div = round(win_shares / int(wins),2)
        #we append values to this list
        y_vals_all.append(div)
    
    #----------We plot every players win/total_team_wins value here
    #----------and a legend, and show the scatter plot
    #----------and we also remove the x values, because they look too close together
    plt.scatter(x_vals_all, y_vals_all,label="players from 2018-2019 season")
    plt.legend(loc="upper right",prop={'size': 20})
    plt.xticks([])
    plt.show()

if __name__=="__main__":
    main()
