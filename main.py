from flask import Flask, Response, request
import pull_iex
import visual
app = Flask(__name__)


@app.route('/')
def hello():
    return f"""
    <h1><u>Generate Intraday Graphs</u></h1>
    <h3><pre class="tab">
Ticker Selection        Ticker2 Selection        Y-Axis Selection</h3>
    <form method="POST">
        <input name="ticker1">
        <input name="ticker2">
        <input name="text3">
        <input type="submit">
    </form>
    <h2><pre class="tab">
<u>Sample Values:</u><br />
GOOG              AMZN              Volume<br />
TSLA              PGM               Average<br />
AMD               WMT               Open<br />
WMT               AMD               Close<br />
PGM               TSLA              High<br />
AMZN              TSLA              Low<br />
    </h2>
    <h2><pre class="tab">
<u>Default Values:</u><br />
SPY               QQQ              Volume</h2>
<h3>Plot as a png</h3>
    <img src='/', methods=['POST']
         alt="random points as png"
         height="200"
    >
"""


@app.route('/', methods=['POST'])
def my_form_post(list_tickers=['SPY', 'QQQ'], req='2', y_value='Volume'):
    if request.form.get("ticker1"):
        list_tickers = [request.form.get(
            "ticker1"), request.form.get("ticker2")]
    if request.form.get("text3"):
        y_value = request.form.get("text3")
    return visual.intraday_visual_pipeline(list_tickers, req, y_value)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
