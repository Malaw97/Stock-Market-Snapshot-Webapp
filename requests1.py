import requests
from bs4 import BeautifulSoup
import json

r = requests.get('https://finance.yahoo.com/quote/TSLA?p=TSLA')

soup = BeautifulSoup(r.text,'lxml')

g=soup.find_all('span',{'class':'Trsdu(0.3s)','class':'Fw(b)'})
# for i in g:
    # print(i.text)

# ticker = input("What ticker(s) would you like to explore (If entering more than one, separate each ticker by a comma)? ")
ticker='tsla'
key= 'Tpk_fff49e874d4a452b8a9c636ff96b06bc'
url=requests.get('https://sandbox.iexapis.com/stable/stock/' + ticker + '/quote?token=' + key)

soup = BeautifulSoup(url.text,'lxml')
url_data=(soup.find('body',{'style':''})).text

json_acceptable_string = url_data.replace("'", "\"")
print(json_acceptable_string)
d = json.loads(json_acceptable_string)
print(d)