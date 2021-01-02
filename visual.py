from flask import Flask, Response, request
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.backends.backend_svg import FigureCanvasSVG
import matplotlib.pyplot as plt
import pandas as pd
import io

import pull_iex


def req_sort(req):
    if req == '2':
        return 'Intraday '


def intraday_visual_pipeline(list_tickers, req, y_value):
    list_tickers = [i.strip() for i in list_tickers]
    req_type = req_sort(req)
    fig, ax = plt.subplots()
    data = [dataset for dataset in pull_iex.main(list_tickers, req)]
    for i in range(len(list_tickers)):
        ax.plot((data[i]['minute']), (data[i][y_value.lower()]),
                label=list_tickers[i].upper())

    ax.set(xlabel='Time (m)', ylabel=y_value,
           title=req_type+y_value+' over Time')
    ax.grid()
    plt.legend()
    output = io.BytesIO()
    FigureCanvasAgg(fig).print_png(output)
    return Response(output.getvalue(), mimetype="image/png")


#print(intraday_visual_pipeline(['airi', 'amd', 'ba', 'bmo', 'bns','nclh', 'pgm', 'ry', 'wmt', 'spy'], '2', 'Volume'))
