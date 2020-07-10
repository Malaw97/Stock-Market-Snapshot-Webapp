from bs4 import BeautifulSoup
from selenium import webdriver
import chromedriver_binary

#State your designated ticker
tickers=input("What ticker(s) would you like to explore (If entering more than one, separate each ticker by a comma)? ")

def parse_input(ticker_list):
    ticks=[]
    ticker_list=ticker_list.split(',')
    for i in ticker_list:
        ticks.append(i.strip())
    return ticks

def return_data(ticker):
    '''
    Return data associated with a given ticker
    '''
    #Open chromedriver.exe
    webdrive=webdriver.Chrome(r'D:\Documents\Github\Scraper\chromedriver.exe')
    #Assign designated ticker to hyperlink
    webdrive.get('https://finance.yahoo.com/quote/'+ticker+'/financials?p='+ticker)
    html = webdrive.execute_script('return document.body.innerHTML;')
    soup = BeautifulSoup(html,'lxml')
    Price = [i.text for i in soup.find_all('span', {'class':'Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)'})]
    DoD_Change = [i.text for i in soup.find_all('span', {'class':'Trsdu(0.3s) Fw(500) Pstart(10px) Fz(24px) C($positiveColor)'})]

    data=[ticker.upper(), float((Price[0]).replace((','),(''))), DoD_Change[0]]
    return data

def main():
    l=[]
    for i in parse_input(tickers):
        l.append(return_data(i))
    return l

print(main())
