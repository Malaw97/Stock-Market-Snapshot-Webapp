import requests
from bs4 import BeautifulSoup
import json

# user_input = input("What ticker(s) would you like to explore (If entering more than one, separate each ticker by a comma)? ")
user_input='tsla, amzn, aapl'

def parse_input(tickers):
    ticker_list=[]
    tickers=tickers.split(',')
    for i in tickers:
        ticker_list.append(i.strip())
    return ticker_list

def retrieve(ticker):
    '''
    Return data associated with a given ticker
    '''
    key= 'Tpk_fff49e874d4a452b8a9c636ff96b06bc'
    url=requests.get('https://sandbox.iexapis.com/stable/stock/' + ticker + '/quote?token=' + key)

    soup = BeautifulSoup(url.text,'lxml')
    url_data=(soup.find('body',{'style':''})).text

    json_acceptable_string = url_data.replace("'", "\"")
    data = json.loads(json_acceptable_string)
    return data

if __name__=="__main__":
    for i in (parse_input(user_input)):
        print(retrieve(i))