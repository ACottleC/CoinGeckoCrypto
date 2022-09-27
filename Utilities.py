import pandas as pd
import os
from pycoingecko import CoinGeckoAPI


class Utilities:
    @staticmethod
    def export_excel(dataframe, file_name):
        dataframe.to_excel('data/' + file_name + '.xlsx', index=False)
    @staticmethod
    def convert_string_date(datestring):
        #result = time.mktime(datetime(2012, 1, 1, 0, 0).timetuple())
        result = time.mktime(datetime(datestring).timetuple())
        return result

    @staticmethod
    def is_valid_coin(coin, coin_list):
        #We check wheter is an id, symbol or name
        for i in coin_list:
            if i['id'] == coin:
                print('The coin is an id.')
                return coin
            elif i['symbol'] == coin:
                print('The coin is a symbol.')
                return coin_list[i].get('id')
            elif i['name'].lower() == coin.lower():
                print('The coin is a name.')
                return coin_list[i].get('id')
        #if we don't find the coin, we return false
        print('The coin was not found.')
        return False
