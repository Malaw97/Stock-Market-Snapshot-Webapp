import requests
import json
from bs4 import BeautifulSoup
import pandas as pd
from decouple import config


def take_user_input():
    '''
    Take 2 inputs from user, cleaning and verifying retrieval type validity
    Raise assertion error if retrieval type is invalid
    Extract api key from .env file
    '''
    user_input = input(
        "What ticker(s) would you like to explore? (If entering more than one, separate each ticker by a comma)\n ")
    # Clean ticker input
    user_input = parse_input(user_input)
    user_input2 = (
        input("Retrieval Type?\n 1 => Quote\n 2 => Intraday-Prices\n")).strip()
    # Check validity of retrieval type
    assert user_input2.isdigit(), "Invalid entry"
    # Retrieve api key from .env file
    api_key = config('Test_Key_1')
    # Place inputs into a list
    user_inp = [user_input, user_input2, api_key]
    return user_inp


def parse_input(tickers):
    '''
    Clean input, returning a readable list
    '''
    ticker_list = []
    tickers = tickers.split(',')
    for i in tickers:
        i = i.strip()
        ticker_list.append(i)
    return ticker_list


def request_sort(num):
    '''
    Map numbers to retrieval types. Used to access proper url
    '''
    if num == '1':
        return 'quote'
    elif num == '2':
        return 'intraday-prices'
    elif num == '3':
        return ''
    else:
        assert False, "Invalid Numeric Entry"


def retrieve(ticker, request1, key):
    '''
    Return dictionary interpretation of json data associated with a given ticker
    Raise assertion error if ticker is invalid
    '''
    # Connect to and process a url's html data
    url = requests.get(
        'https://sandbox.iexapis.com/stable/stock/' +
        ticker +
        '/' +
        request1 +
        '?token=' +
        key)
    soup = BeautifulSoup(url.text, 'lxml')
    # Locate chosen string within HTML
    url_data = (soup.find('body', {'style': ''})).text
    assert url_data!='Unknown symbol', 'Invalid Ticker'
    # Transform into json data
    json_acceptable_string = url_data.replace("'", "\"")
    # Turn into python object
    json_data = json.loads(json_acceptable_string)
    return json_data


def format_data(user_input2, json_data):
    '''
    Format json data into dataframes
    '''
    #keys, values =list(data.keys()),list(data.values())
    #df=pd.DataFrame({'Keys': keys, 'Values': values})
    if user_input2 == "1":
        # Convert singular dictionary into dataframe
        # Return a list
        df = pd.DataFrame(json_data, index=[1])
        return df
    elif user_input2 == "2":
        # Convert multiple dictionaries to dataframes, appending them to a list
        # Return a list of dataframes
        list_df = []
        for i in json_data:
            df = pd.DataFrame(i, index=[0])
            list_df.append(df)
        df = pd.concat(list_df)
        df.reset_index(drop=True, inplace=True)
        return df


def package_retrieve(user_inp):
    '''
    This is the main function
    Package df based on user_input2 (Retrieval Type)
    Sample input: package_retrieve(["tsla, amzn", "1", "Tpk_fff49e874d4a452b8a9c636ff96b06bc"])
    '''
    # Assign list of inputs to variables
    user_input, user_input2, key = user_inp[0], user_inp[1], user_inp[2]
    list_df = []
    for i in (user_input):
        # Produce list of dataframes
        request_type = request_sort(user_input2)
        json_data = (retrieve(i, request_type, key))
        data = format_data(user_input2, json_data)
        list_df.append(data)
    if user_input2 == '1':
        # Return list containing one dataframe
        list_df = pd.concat(list_df)
        list_df.reset_index(drop=True, inplace=True)
        return list_df
    elif user_input2 == '2':
        # Return the list of dataframes
        return list_df


if __name__ == "__main__":
    output = package_retrieve(take_user_input())
    print(output)
