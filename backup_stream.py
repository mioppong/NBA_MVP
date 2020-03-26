from textblob import TextBlob
import tweepy
import sys
import time
import psutil
import matplotlib.pyplot as plt
import numpy as np
import random
from itertools import count 
import random
import os
import config

#authentication needed for twitter
auth = tweepy.OAuthHandler(config.api_key,config.api_secret)
auth.set_access_token(config.access_token,config.token_secret)
api = tweepy.API(auth)

class MyStreamListener(tweepy.StreamListener):
    #this method is called everytime there is a tweet
    #basically everytime we see a hashtag, increment each hashtag counter by 1

    blob = ""
    y_vals = {}
    def on_status(self,status):
        
        with open("prediction_just_names.txt", 'r') as f, open("plot_this.txt", 'w+') as plot_file:

            for i,player in enumerate(f):
                player = player.strip()
                self.y_vals[player] = 0.0
                if player in status.text:
                    self.blob = TextBlob(status.text)
                    self.y_vals[player] += self.blob.sentiment.polarity
                    print(player+'\t'+str(round(self.y_vals[player],6)))

                    for x in list(self.y_vals.keys()):
                        plot_file.write(x +','+ str(self.y_vals[x])+'\n')
                
            
            

    def on_error(self, status_code):
        if status_code == 420:
            print("ERRORRRRR")
            return False

def main():

    my_stream_listener = MyStreamListener()
    players = []
    
    #---------- we just get first and last name 
    #----------of player and store it in players
    with open("prediction.txt") as f:
        for text in f:
            player_name,dont,care = text.partition('\n')
            players.append(player_name)
    
    
    #with open("prediction_just_names.txt", 'w+') as f:
     #   for player in players:
      #      f.write(player+ '\n')

    my_stream = tweepy.Stream(auth, listener=my_stream_listener)
    my_stream.filter(track=players,is_async=True)


if __name__ == "__main__":
    main()
