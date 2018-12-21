import  os
import json
import time
import requests
from datetime import datetime

convert = "USD"

listing_url = 'https://api.coinmarketcap.com/v2/listings/?convert=' + convert
url_end = '?structure=array&convert=' + convert
request = requests.get(listing_url)
results = request.json()
data = results['data']

print(json.dumps(results, sort_keys=True, indent=4))

ticker_url_pairs = {}
for currency in data:
    symbol = currency['symbol']
    url = currency['id']
    ticker_url_pairs[symbol] = url

print()
print('Alert Tracking ...')
print()

already_hit_symbols = []

while True:
    with open('alerts.txt') as inp:
        for line in inp:
            ticker, amount = line.split()
            ticker = ticker.upper()
            ticler_url = 'https://api.coinmarketcap.com/v2/ticker/' + str(ticker_url_pairs[ticker]) + '/' + url_end

            request = requests.get(ticler_url)
            results = request.json()

            currency = results['data'][0]

            name = currency['name']
            symbol = currency['symbol']
            last_updated = currency['last_updated']

            quotes = currency['quotes'][convert]
            market_cap = quotes['market_cap']
            price = quotes['price']
            price_string = '{:,}'.format(round(price,2))
            market_cap_string = '{:,}'.format(market_cap)

            if float(price) >= float(amount) and symbol not in already_hit_symbols:
                os.system('say ' +name+ " hit " + price_string + " "+ str(convert))
                last_updated_str = datetime.fromtimestamp(last_updated).strftime('%B %d, %Y at %I:%M%p')
                print(name + ' hit ' + price_string + ' on ' + last_updated_str)
                already_hit_symbols.append(symbol)
    print('...')
    already_hit_symbols = []
    time.sleep(500)
