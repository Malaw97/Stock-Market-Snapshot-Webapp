import requests, json, sys
from bs4 import BeautifulSoup
import pandas as pd
from decouple import config

def take_user_input():
    '''
    '''
    user_input = input("What ticker(s) would you like to explore? (If entering more than one, separate each ticker by a comma)\n ")
    user_input2 = (input("Retrieval Type?\n 1 => Quote\n 2 => Intraday-Prices\n")).strip()
    api_key=config('Test_Key_1')
    


def parse_input(tickers):
    '''
    Clean input, placing in a readable list format
    '''
    ticker_list=[]
    tickers=tickers.split(',')
    for i in tickers:
        i=i.strip()
        if len(i)!=4:
            print('Invalid Ticker Length')
            sys.exit()
        else:
            ticker_list.append(i)
    return ticker_list

def request_sort(num):
    '''
    Map numbers to retrieval types
    '''
    if num=='1':
        return 'quote'
    elif num=='2':
        return 'intraday-prices' 
    elif num=='3':
        return '' 
    else:
        print("Invalid Numeric Entry")
        sys.exit()

def retrieve(ticker, request1, key):
    '''
    Return json data associated with a given ticker
    '''
    url=requests.get('https://sandbox.iexapis.com/stable/stock/' + ticker + '/' + request1 + '?token=' + key)
    soup = BeautifulSoup(url.text,'lxml')
    url_data=(soup.find('body',{'style':''})).text

    json_acceptable_string = url_data.replace("'", "\"")
    json_data = json.loads(json_acceptable_string)
    return json_data

def format_data(json_data):
    '''
    Format json data into dataframes
    '''
    if user_input2=="1":
    #     keys, values =list(data.keys()),list(data.values())
    #     df=pd.DataFrame({'Keys': keys, 'Values': values})
        df=pd.DataFrame(json_data,index=[1])
        return df
    elif user_input2=="2":
        list_df=[]
        for i in json_data:
            df=pd.DataFrame(i,index=[0])
            list_df.append(df)
        df=pd.concat(list_df)
        df.reset_index(drop=True, inplace=True)
        return df

def package_retrieve(user_input, user_input2, key):
    '''
    Package df based on user_input2 (Retrieval Type)
    '''
    list_df=[]
    for i in (parse_input(user_input)):
        request_type=request_sort(user_input2)
        json_data=(retrieve(i, request_type, key))
        data=format_data(json_data)
        list_df.append(data)
    if user_input2=='1':
        list_df=pd.concat(list_df)
        list_df.reset_index(drop=True, inplace=True)
        return list_df
    elif user_input2=='2':
        return list_df

def graph():
    '''
    Return visual representation of a dataframe
    '''

if __name__=="__main__":
    output=package_retrieve(take_user_input())
    print(output)