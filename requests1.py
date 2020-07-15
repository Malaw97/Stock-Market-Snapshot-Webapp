import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import sys

user_input = input("What ticker(s) would you like to explore (If entering more than one, separate each ticker by a comma)?\n ")
user_input2 = input("Retrieval Type?\n 1 => Quote\n 2 => Intraday-prices\n")

# user_input='tsla, amzn, aapl'
key= 'Tpk_fff49e874d4a452b8a9c636ff96b06bc'

def parse_input(tickers):
    '''
    Clean input, placing in a readable list format
    '''
    ticker_list=[]
    tickers=tickers.split(',')
    for i in tickers:
        ticker_list.append(i.strip())
    return ticker_list

def request_type(num):
    '''
    Map numbers to retrieval types
    '''
    num=num.strip()
    if num=='1':
        return 'quote'
    elif num=='2':
        return 'intraday-prices'
    else:
        print("Invalid Numeric Entry")
        sys.exit()

def retrieve(ticker, request1):
    '''
    Return data associated with a given ticker
    '''
    url=requests.get('https://sandbox.iexapis.com/stable/stock/' + ticker + '/' + request1 + '?token=' + key)
    soup = BeautifulSoup(url.text,'lxml')
    url_data=(soup.find('body',{'style':''})).text

    json_acceptable_string = url_data.replace("'", "\"")
    data = json.loads(json_acceptable_string)
    return data


if __name__=="__main__":
    for i in (parse_input(user_input)):
        if len(i)==4:
            print(retrieve(i, request_type(user_input2)))
        else:
            print('Invalid Ticker Length')
            sys.exit()