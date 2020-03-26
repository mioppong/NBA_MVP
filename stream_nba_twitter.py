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
import pandas as pd
import sys
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from matplotlib.ticker import FormatStrFormatter


#authentication needed for twitter
auth = tweepy.OAuthHandler(config.api_key,config.api_secret)
auth.set_access_token(config.access_token,config.token_secret)
api = tweepy.API(auth)

players = []
streamed_dict = {}
df = pd.DataFrame(streamed_dict)

style.use('fivethirtyeight')
fig  = plt.figure()
fig.suptitle('Players with potential to win MVP', fontsize=14, fontweight='bold')
ax1 = fig.add_subplot(1,1,1)
ax1.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))


class MyStreamListener(tweepy.StreamListener):
    #this method is called everytime there is a tweet
    #basically everytime we see a hashtag, increment each hashtag counter by 1

    blob = ""
    y_vals = {}
    def on_status(self,status):
        for x in players:
            if x in status.text:
                if x not in streamed_dict.keys():
                    streamed_dict[x] = 0
                else:
                    self.blob = TextBlob(status.text)
                    streamed_dict[x] += self.blob.sentiment.polarity
                    streamed_dict[x] = round(streamed_dict[x],2)
        
    def on_error(self, status_code):
        if status_code == 420:
            print("ERRORRRRR")
            return False

def animate(i):
    ax1.cla()
    ax1.plot(list(streamed_dict.values()),list(streamed_dict.keys()))
    ax1.set_ylabel('MVP candidates (based on my algirithm) for')

    #ax1.set_ylabel("y axis",fontsize=0.5)

my_stream_listener = MyStreamListener()

#---------- we just get first and last name 
#----------of player and store it in players
with open("prediction.txt") as f:
    for text in f:
        player_name,dont,care = text.partition('\n')
        players.append(player_name)

my_stream = tweepy.Stream(auth, listener=my_stream_listener)
my_stream.filter(track=players,is_async=True)

#basically after 500ms, update my graph
ani = animation.FuncAnimation(fig, animate, interval=100)
plt.show()
animate(2)