#!/usr/bin/env python
# coding: utf-8

# # API Test Notebook

#This example uses Python 2.7 and the python-request library.

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import datetime

url = 'https://sandbox-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

#PRO Environment URL url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
#use the pro environment when you have created an account with CoinMarketcap.com
# API Key for AlextheAnalyst example '0ad53085-1cb2-4eb8-ad9e-3ffbd7e56509'

parameters = {
  'start':'1',
  'limit':'5000',
  'convert':'USD'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': 'b54bcf4d-1bca-4e8e-9a24-22ff2c3d462c',
}

session = Session()
session.headers.update(headers)

try:
  response = session.get(url, params=parameters)
  data = json.loads(response.text)
  print(data)
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)

type(data)

import pandas as pd

pd.set_option('display.max_columns', None) #adjust the setting to show all columns

pd.json_normalize(data['data']) #takes the raw json data and put it into a dataframe view

#this normalizes the data and makes it all pretty in the dataframe

df = pd.json_normalize(data['data']) #assign the data to the dateframe df
df['timestamp'] = datetime.datetime.now() #insert a timestamp within the dateframe
df

def api_runner():
    global df #declare a global variable
    
    url = 'https://sandbox-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

    #PRO Environment URL url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    #use the pro environment when you have created an account with CoinMarketcap.com
    # API Key for AlextheAnalyst example '0ad53085-1cb2-4eb8-ad9e-3ffbd7e56509'

    parameters = {
      'start':'1',
      'limit':'5000',
      'convert':'USD'
    }
    headers = {
      'Accepts': 'application/json',
      'X-CMC_PRO_API_KEY': 'b54bcf4d-1bca-4e8e-9a24-22ff2c3d462c',
    }

    session = Session()
    session.headers.update(headers)

    try:
      response = session.get(url, params=parameters)
      data = json.loads(response.text)
      #print(data)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
      print(e)
    
    #df2 = pd.json_normalize(data['data']) #assign the data to the dateframe df
    #df2['timestamp'] = datetime.datetime.now() #insert a timestamp within the dateframe
    ##df = df.append(df2) #depreicated way to append
    #frames = [df, df2]
    #df = pd.concat([df,df2])

    df = pd.json_normalize(data['data'])
    df['timestamp'] = datetime.datetime.now()
    df  
    
    
    if not os.path.isfile(r'/Users/Documents/py_api/API.csv'): #checks to see if the files exisits
        df.to_csv(r'/Users/Documents/py_api/API.csv', header ='column_names')
    else:
        df.to_csv(r'/Users/Documents/py_api/API.csv', mode='a', header=False)

import os
import pandas as pd
from time import time
from time import sleep

for i in range(12):
    print('Before Runner')
    api_runner()
    print('API Runner completed successfully')
    sleep(60) #sleep for 1 minute
exit()

df72 = pd.read_csv(r'/Users/Documents/py_api/API.csv')
df72

pd.set_option('display.float_format', lambda x: '%.5f' % x) #this line of code adjusts the view of float values to display up to 5 decimal places

df

df3 = df.groupby('name',sort=False)[['quote.USD.percent_change_1h','quote.USD.percent_change_24h','quote.USD.percent_change_7d']].mean()
df3

df4 = df3.stack() #pivots the df3 dataframe to create rows from the column data
df4

type(df4) #displays that dataframe 4 is now a Series

df5 = df4.to_frame(name='values')
df5

type(df5)
df5.count()

#want to give df5 an index
index = pd.Index(range(30))

df6 = df5.reset_index()
df6

df7 = df6.rename(columns={'level_1':'percent change'}) #rename the column
df7

df7['percent change'] = df7['percent change'].replace(['quote.USD.percent_change_1h','quote.USD.percent_change_24h','quote.USD.percent_change_7d'],['1hr','24h','7d'])
df7

import seaborn as sns
import matplotlib.pyplot as plt

sns.catplot(x='percent change', y='values', hue='name', data=df7, kind='point')

df8 = df[['name','symbol','max_supply','timestamp']]
df8 = df8.query("name == '6ra70mhw2sj'") #query the data frame to pull out a specific name
df8

df9 = df[['name','symbol','max_supply','timestamp']]
df9 = df8.query("name == '6ra70mhw2sj' | name == 'tk8n4a67zcf'") #query the data frame to pull out a specific name
df9

sns.set_theme(style="darkgrid")
sns.lineplot(x='timestamp',y='name', data=df8)