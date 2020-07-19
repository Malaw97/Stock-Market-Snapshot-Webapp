import asyncio
import json
import requests
from bs4 import BeautifulSoup
import time


async def fetch():
    url = requests.get('https://sandbox.iexapis.com/stable/stock/tsla/intraday-prices?token=Tpk_fff49e874d4a452b8a9c636ff96b06bc')
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
    # Transform into json data
    json_acceptable_string = url_data.replace("'", "\"")
    # Turn into python object
    json_data = json.loads(json_acceptable_string)
    return json_data
t1=time.time()
async def one():
    url=fetch()
    g = await url
    print('THIS TOOK ' , time.time()-t1)


loop=asyncio.get_event_loop()
loop.run_until_complete(one())
print('ASYNC FUNC TOOK' , time.time()-t1)

t1=time.time()
def fetch():
    url = requests.get('https://sandbox.iexapis.com/stable/stock/tsla/intraday-prices?token=Tpk_fff49e874d4a452b8a9c636ff96b06bc')
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
    # Transform into json data
    json_acceptable_string = url_data.replace("'", "\"")
    # Turn into python object
    json_data = json.loads(json_acceptable_string)

fetch()
print('SECOND FUNC TOOK ' , time.time()-t1)