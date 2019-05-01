
from flask import Flask, render_template
import requests
import time

app = Flask(__name__, template_folder="templates")


def get_data(url, dir, dir2):
	while True: 
	    api_response = requests.get(url)
	    if api_response.status_code != 200:
	        api_price = 'error'
	    else:
	        api_data = api_response.json()
	        if dir2 != 0:
	            api_price = api_data[dir][dir2]
	        else:
	            api_price = api_data[dir]
	        api_price = float(api_price)
	        api_price = round(api_price, 2)
	        return api_price
	    time.sleep(60)

def unit_dif(p, cb):
    if isinstance(p, str) == True:
        return "---"
    else:
        result = round(p - cb, 2)
        return result

def percent_dif(p, cb):
    if isinstance(p, str) == True:
        return "---"
    else:
        result = round(((p - cb) / cb) * 100, 2)
        return result
def twd_usd(p, decimal):
    if isinstance(p, str) == True:
        return "___"
    else:
        result = round(p / 30.8, decimal)
        return result


cb_price = get_data("https://api.coinbase.com/v2/prices/BTC-USD/buy", "data", "amount") 
mc_price = get_data("https://api.maicoin.com/v1/prices/USD", "buy_price", 0)
bito_price = get_data("https://www.bitoex.com/api/v1/get_rate", "buy", 0)
bito_price = twd_usd(bito_price, 2)
mc_perc_diff = percent_dif(mc_price, cb_price)
mc_unit_diff = unit_dif(mc_price, cb_price)
bito_perc_diff = percent_dif(bito_price, cb_price)
bito_unit_diff = unit_dif(bito_price, cb_price)






@app.route("/hello")
def hello():
	return "Hello there, Gerneral Kenobi!"

@app.route("/")
@app.route("/index")
def index():
    user = {'username': "anon"}
    posts = [
        {
            
            'market' : 'BitoEx',
            'price' : bito_price,
            'unit_diff' : bito_unit_diff,
            'percent_diff' : bito_perc_diff,
            'location' : '../static/style/img/facesbito-logo.png',
            'link' : "https://www.bitoex.com/",
            'btn_name' : 'BUY NOW'
        },
        {
            'market' : 'Coinbase',
            'price' : cb_price,
            'unit_diff' : '0',
            'percent_diff' : '0',
            'location' : '../static/style/img/facescb-logo.png',
            'link' : '#',
            'btn' : 'disabled',
            'btn_name' : 'Unavailable in TW'
        },
       {
            'market' : 'MaiCoin',
            'price' : mc_price,
            'unit_diff' : mc_unit_diff,
            'percent_diff' : mc_perc_diff,
            'location' : '../static/style/img/facesmc-logo.png',
            'link' : 'https://www.maicoin.com/en',
            'btn_name' : 'BUY NOW'
        }
        
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)



if __name__ == "__main__":
	app.run(debug=True)
