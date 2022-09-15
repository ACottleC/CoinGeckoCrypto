import sys
import time
import requests
import matplotlib.pyplot as plt
import pandas as pd
from pycoingecko import CoinGeckoAPI

# We call the API to retrieve all the information of the available coins - pagination is 250

response = CoinGeckoAPI().get_coins_markets('usd', per_page=250, price_change_percentage='24h', page=1)
coins_list_df = pd.DataFrame.from_dict(response)
x = 1
print('X is equal to: ' + str(x) + ' Length of the list is: ' + str(len(coins_list_df)))

while len(response) != 0:
    x = x + 1
    response = CoinGeckoAPI().get_coins_markets('usd', per_page=250, price_change_percentage='24h', page=x)
    coins_list_df = pd.concat([coins_list_df, pd.DataFrame.from_dict(response)], ignore_index=True)
    print('X is equal to: ' + str(x) + ' Length of the list is: ' + str(len(coins_list_df)) + ' response len: ' + str(len(response)))

#We export the data to an excel file
combined_df.to_excel('data/CoinList.xlsx', index=False)
