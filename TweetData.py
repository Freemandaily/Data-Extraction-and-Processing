import time
import tweepy
import sys
from datetime import timedelta
import datetime
import pytz,re
import json,os
import streamlit as st

bearerToken = st.secrets('BEARERTOKEN')

class processor:
    def __init__(self) -> None: # Default 7 days TimeFrame
        self.client =  tweepy.Client(bearerToken)
        self.client =  tweepy.Client(bearerToken)
        self.username = None
        self.user = None
        self.user_id = None
        self.timeframe = None
        self.end_date = None
        self.start_date = None
    
    def Load_user(self,username,timeframe=7):
        self.username = username
        self.timeframe = timeframe
        try:
            self.user = self.client.get_user(username=username)
            self.user_id = self.user.data.id
            self.end_date = datetime.datetime.now(pytz.UTC).replace(microsecond=0)
            self.start_date = (self.end_date - timedelta(days=timeframe)).replace(hour=0,minute=0,second=1,microsecond=0)
            st.toast(f'@{username} Handle Successfully Loaded')
            time.sleep(5)
            return {'Success':True}
        except Exception as e:
            time.sleep(2)
            Error_message = {'Error':f'Error: {e}\n.Upgrade Your X Developer Plan or Try Again Sometimes'}
            return Error_message
        
    
    # Fetching Ticker and contracts contains in the tweet
    def fetchTicker_Contract(self,tweet_text:str) -> dict:
        contract_patterns = r'\b(0x[a-fA-F0-9]{40}|[1-9A-HJ-NP-Za-km-z]{32,44}|T[1-9A-HJ-NP-Za-km-z]{33})\b'
        ticker_partterns = r'\$[A-Za-z0-9_-]+'

        token_details = {
            'ticker_names' : re.findall(ticker_partterns,tweet_text),
            'contracts' : re.findall(contract_patterns,tweet_text) 
        }
        return token_details

    # Using X API to fetch user tweets
    def fetchTweets(self) -> list:
        user_tweets =  [{'created_at':'2025-04-22 14:27:35',
                        'tweet_text':'ths is the man he said that kills $Ray '}
                        ]
        # user_tweets = []
        # try:
        #     for response in tweepy.Paginator(self.client.get_users_tweets,
        #                                     id=self.user_id,
        #                                     start_time=self.start_date, 
        #                                     end_time=self.end_date,
        #                                     exclude='replies',
        #                                     max_results=100,
        #                                     limit=1, # consider this
        #                                     tweet_fields='created_at'):
        #         if response.data:
        #             for tweet in response.data:
        #                 tweet_dict = {
        #                     'tweet_id':tweet.id,
        #                     'tweet_text':tweet.text,
        #                     'created_at':tweet.created_at.strftime("%Y-%m-%d %H:%M:%S")
        #                 }
        #                 user_tweets.append(tweet_dict)
        #     #print(user_tweets)
        #     return user_tweets
        # except Exception as e:
        #     Error_message = {'Error':f'Failed To Fetch Tweets Because of  {e}\nUpgrade Your X Developer Plan or Wait For Sometimes'}
        #     return Error_message
        return user_tweets
        
    # format the data to a suitable data type
    def Reformat(self,fetched_Token_details:list) -> dict:
        details = {}
        for data in fetched_Token_details:
            details[data['date']] = { 'Token_names': data['token_details']['ticker_names'],
                                       'contracts': data['token_details']['contracts']}
        details = {date: tokenName_contract for date,tokenName_contract in details.items() if tokenName_contract['Token_names'] or tokenName_contract['contracts']}
        if details:
            st.toast('Tweets Containing Token Symbols Found!')
            time.sleep(10)
            print('Tweets Containing Token Symbols Found!')
            return details
        else:
            Error_message = {'Error':'No Tweets Contain Any Token Symbols Or CA.\nAdjust Timeframe and Try Again'}
            time.sleep(7)
            return Error_message
        
    # Start procesing user tweet
    def processTweets(self)->dict: # Entry function
        tweets = self.fetchTweets()
        if isinstance(tweets,dict) and 'Error' in tweets:
            return tweets # Error handlig for streamlit
        fetched_Token_details = []
    
        if tweets:
            for tweet in tweets:
                token_details = self.fetchTicker_Contract(tweet['tweet_text'])
                refined_details = {
                    'token_details': token_details,
                    'date': tweet['created_at']
                }
                fetched_Token_details.append(refined_details)
            tweeted_Token_details = self.Reformat(fetched_Token_details)
            return tweeted_Token_details
        else :
            Error_message = {'Error':f'Not Able To Process {self.username} Tweets'}
            return Error_message
