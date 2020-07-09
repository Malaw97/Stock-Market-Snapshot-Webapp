import pandas as pd
from bs4 import BeautifulSoup
import re
from selenium import webdriver
import chromedriver_binary
import string
pd.options.display.float_format = '{:.0f}'.format

ticker=input("What ticker? ")
create_link = 'https://finance.yahoo.com/quote/AAPL/financials?p='+ticker
driver = webdriver.Chrome('D:\Documents\Github\chromedriver.exe')
driver.get(create_link)
html = driver.execute_script('return document.body.innerHTML;')
soup = BeautifulSoup(html,'lxml')