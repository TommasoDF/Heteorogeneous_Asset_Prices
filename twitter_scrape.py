###Imports
import os, subprocess, json, csv, uuid
import time as tm
import pandas as pd
import numpy as np
from datetime import date, time
import snscrape.modules.twitter as sntwitter

#Defining the paramentes
start = date(2020, 12, 5) #Starting period
start = start.strftime('%Y-%m-%d') #Converting into datetime format

stop = date(2021, 10, 4) #Ending period 
stop = stop.strftime('%Y-%m-%d')

#Converting into datetime format
#Keyword
keyword = 'Bitcoin'
#Max numbers of Tweets
maxTweets = 10**1
#inizializing an empy list
tweets_list = []

# Using TwitterSearchScraper to scrape data and append tweets to list

loop_start = tm.time()


for i,tweet in enumerate(sntwitter.TwitterSearchScraper(keyword + ' since:' + start + ' until:' + stop + ' -filter:links' + ' -filter:replies').get_items()):
    if i>maxTweets:
        break
    tweets_list.append([tweet.date, tweet.id, tweet.rawContent, tweet.user.username])
loop_end= tm.time()
total_time = loop_end - loop_start
print("execution time was:",str(total_time))

tweets_list



#Creating a df
tweets_df = pd.DataFrame(tweets_list, columns=['Datetime', 'Tweet Id', 'Text', 'Username'])
start_day = tweets_df.Datetime.iloc[0].strftime('%Y-%m-%d_%H-%M-%S')
end_day = tweets_df.Datetime.iloc[-1].strftime('%Y-%m-%d_%H-%M-%S')




tweets_df.to_csv(keyword + '_from_'+ start_day + '_to_'+ end_day + '.csv')

