import requests
import json
import time

postfix_usdt = 'USDT'
postfix_rub = 'RUB'

exchange_sum_rub = 100000

input_rub = float(exchange_sum_rub)

result = open("ex_coins_result.json", "w")
result_arr = []

coins_file = open("res/ex_coins", "r")
coins_arr = coins_file.read().split('\n')
coins_file.close()

requests.adapters.DEFAULT_RETRIES = 20  # increase retries number
s = requests.session()
s.keep_alive = False  # disable keep alive

response_rub2usdt = s.get('https://api.binance.com/api/v3/trades', params={'symbol': 'USDTRUB', 'limit': '1'}).json()
rub2usdt = input_rub / float(response_rub2usdt[0]['price'])
print('RUB to USDT: ' + str(rub2usdt))

for coin in coins_arr:
    rub2coin = coin + postfix_rub
    coin2usdt = coin + postfix_usdt

    query_rub2coin = {'symbol': rub2coin, 'limit': '1'}
    query_coin2usdt = {'symbol': coin2usdt, 'limit': '1'}

    response_rub2coin = s.get('https://api.binance.com/api/v3/trades', params=query_rub2coin).json()
    time.sleep(1)
    response_coin2usdt = s.get('https://api.binance.com/api/v3/trades', params=query_coin2usdt).json()
    time.sleep(1)

    to_coin = float(response_rub2coin[0]['price'])
    to_usdt = float(response_coin2usdt[0]['price'])

    result_usdt = (input_rub / to_coin) * to_usdt
    ex_result = (rub2coin, coin2usdt, result_usdt)
    result_arr.append(ex_result)

    print(rub2coin + ' -> ' + coin2usdt + ' ' + str(result_usdt))

result_arr_sorted = sorted(result_arr, key=lambda tup: tup[2], reverse=True)

result.write(json.dumps(result_arr_sorted))
result.close()

for r in result_arr_sorted:
    print(r)
