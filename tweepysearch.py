from cgitb import text
import os
import tweepy
import pandas as pd
import configparser
import time
import datetime
import requests

#clear terminal
os.system("cls")

################
##### SETUP ####
################
#read configs
config = configparser.ConfigParser()
config.read('C:/Users/Gurk/Documents/Python/Twitter Bot v1/config.ini')

#retrieve access info
api_key=config['twitter']['api_key']
api_key_secret=config['twitter']['api_key_secret']
access_token = config['twitter']['access_token']
access_token_secret = config['twitter']['access_token_secret']
bearer= config['twitter']['bearer']

#set up client and authenticate
print("Authenticating...")
client = tweepy.Client(bearer, api_key, api_key_secret, access_token, access_token_secret, wait_on_rate_limit=True)

#Search Parameters
search = '#HouseOfTheDragon lang:en -is: retweet'
filename= search.replace(":","_")
#Client setup
#response = client.search_recent_tweets(query=search, max_results=50, tweet_fields=['created_at', 'lang','author_id','public_metrics'], expansions = ['geo.place_id'])

################
##### DATA ####
################
#vars
tweet_text=[]
tweet_time=[]
tweet_id=[]
tweet_likes=[]
tweet_geo=[]
counter=0

#Go through tweets in client response
print("Fetching Tweets...".center(70,"@"))
with open(f"C:/Users/Gurk/Documents/Python/Twitter Bot v1/{filename}.csv", "a") as outfile:
    print("File opened")
    for tweet in tweepy.Paginator(client.search_recent_tweets, query = search, max_results=100, tweet_fields=['created_at', 'lang','author_id','public_metrics'], expansions = ['geo.place_id']).flatten(limit=10000):

        tweetdf= pd.DataFrame(tweet.data)
        tweet_text.append(tweet.text)
        tweet_time.append(tweet.created_at)
        tweet_id.append(tweet.author_id)
        tweet_likes.append(tweet.public_metrics['like_count'])
        tweet_geo.append(tweet.geo)
        counter+=1
        if counter%500==0:
            print("\n"+"Tweet".center(50,"-"))
            print("Created: ", tweet.created_at)
            print(tweet.text)


print("\n"+"Data Fetch Complete".center(100,"*"))

# Save data as dictionary 
print("Saving Data...")
tweet_df= pd.DataFrame(
    {'tweet': tweet_text,
    'time': tweet_time,
    'id': tweet_id,
    'likes': tweet_likes,
    'location': tweet_geo}
)
print(tweet_df.head())

#Export (to be changed to ammend existing file)
timestamp = pd.to_datetime("today").strftime("%Y%m%d %I%p")
#Dynamic file name using search params and datetime
print("\nSaving as... "+f'{search.replace(":","")} {timestamp}.csv')

tweet_df.to_csv(f'Twitter Archives/{search.replace(":","")} {timestamp}.csv')
