import pull
import matplotlib
import pandas as pd



def main():
    list_df=pull()
    for i in list_df:
        graph(i)