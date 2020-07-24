def install_and_import(package):
    import importlib
    try:
        importlib.import_module(package)
    except ImportError:
        import pip
        pip.main(['install', package])
    finally:
        globals()[package] = importlib.import_module(package)


for i in [
    'requests',
    'json',
    'logging',
    'time',
    'bs4',
    'pandas',
        'concurrent.futures']:
    install_and_import(i)

import requests
import json
import logging
import time
import asyncio
from bs4 import BeautifulSoup
import pandas as pd
from decouple import config
from concurrent.futures import ThreadPoolExecutor

logging.basicConfig(filename='Pull_Errors.log', level=logging.DEBUG)


def take_user_input():
    '''
    FOR TESTING PURPOSES

    Take 2 inputs from user, cleaning and verifying retrieval type validity
    Raise assertion error if retrieval type is invalid
    Extract api key from .env file
    '''
    user_input = input(
        "What ticker(s) would you like to explore? (If entering more than one, separate each ticker by a comma)\n")
    # Clean Ticker Input
    user_input = parse_input(user_input)
    user_input2 = (
        input("Retrieval Type?\n 1 => Quote\n 2 => Intraday-Prices\n")).strip()
    # Place inputs into a list
    user_inp = [user_input, user_input2]
    return user_inp


def parse_input(tickers):
    '''
    FOR TESTING PURPOSES

    Validates take_user_input()
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
        try:
            assert False, "Invalid Retrieval Type"
        except AssertionError as error:
            logging.error(
                'Function: request_sort\n           Error: Invalid Retrieval Request\n           Retrieval Type requested=' +
                num)
            raise


async def get(ticker, user_input2, key):
    '''
    Asynchronously retrieve url data
    Raise assertion error if ticker is invalid
    '''
    time.sleep(0.1)
    executor = ThreadPoolExecutor(2)
    loop = asyncio.get_event_loop()
    # Convert retrieval # to its corresponding retrieval string
    request_type = request_sort(user_input2)
    url = await loop.run_in_executor(executor, requests.get, 'https://sandbox.iexapis.com/stable/stock/' + ticker + '/' + request_type + '?token=' + key)
    soup = BeautifulSoup(url.text, 'lxml')
    # Locate chosen string within HTML
    url_data = (soup.find('body', {'style': ''})).text
    # Check validity of ticker
    try:
        assert url_data != 'Unknown symbol', 'Invalid Ticker Request'
    except AssertionError as error:
        logging.error(
            'Function: retrieve\n           Error: Invalid Ticker Request\n           Ticker Requested=' +
            ticker)
        raise
    return ticker, url_data


def convert(url_data, user_input2, key):
    '''
    Return DataFrame interpretation of json data
    '''
    # Transform into json data
    json_acceptable_string = url_data.replace("'", "\"")
    # Turn into python object-dictionary
    json_data = json.loads(json_acceptable_string)
    # Convert to DataFrame
    if user_input2 == "1":
        # Convert singular dictionary into DataFrame
        # Return a list
        df = pd.DataFrame(json_data, index=[1])
        return df
    elif user_input2 == "2":
        # Convert multiple dictionaries to DataFrames, appending them to a list
        # Return a list of DataFrame
        list_df = []
        for i in json_data:
            df = pd.DataFrame(i, index=[0])
            list_df.append(df)
        df = pd.concat(list_df)
        df.reset_index(drop=True, inplace=True)
        return df


def async_fix(user_input, list_data):
    '''
    Fixes async retrievals resulting in out of order url_data
    '''
    dictionary = {}
    list_df = []
    for i in list_data:
        dictionary[i[0]] = [i[1]]
    for i in user_input:
        list_df.append(dictionary[i][0])
    return(list_df)


async def package_retrieve(user_inp):
    '''
    MAIN FUNCTION
    Package df based on user_input2 (Retrieval Type)
    Sample inputs:
    FOR TESTING: package_retrieve(take_user_input())
    PRODUCTION: package_retrieve([['tsla', 'amzn', 'goog', 'aapl'], '2'])
    '''
    # Retrieve api key from .env file
    user_inp.append(config('Test_Key_1'))
    # Assign list of inputs to variables, and clean ticker input
    user_input, user_input2, key = user_inp[0], user_inp[1], user_inp[2]
    # Output List of DataFrames
    list_df = []
    # Asynchronously retrieve url data
    list_data = await asyncio.gather(*(get(i, user_input2, key) for i in user_input))
    # Fix any possible async ordering issues
    list_data = async_fix(user_input, list_data)
    # For each ticker, add it's requested corresponding DataFrame to a list
    for i in list_data:
        list_df.append(convert(i, user_input2, key))
    if user_input2 == '1':
        # Return list containing one DataFrame
        list_df = pd.concat(list_df)
        list_df.reset_index(drop=True, inplace=True)
        return list_df
    elif user_input2 == '2':
        # Return the list of DataFrame
        return list_df


if __name__ == "__main__":
    t1 = time.time()
    # output = asyncio.run(package_retrieve(take_user_input()))
    output = asyncio.run(package_retrieve(
        [['airi', 'amd', 'ba', 'bmo', 'bns', 'nclh', 'pgm', 'ry', 'wmt', 'spy'], '2']))
    print(output)
    print('Task took %s seconds' % (time.time() - t1))
