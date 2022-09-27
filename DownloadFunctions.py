import sys
import time
import requests
import matplotlib.pyplot as plt
import pandas as pd
from pycoingecko import CoinGeckoAPI
from datetime import datetime


class DownloadFunctions:
    @staticmethod
    def get_coin_prices(coin_id, start_date):
        # Select the start(now) and end times in UNIX format
        if not start_date:
            start_datetime = time.mktime(datetime(2012, 1, 1, 0, 0).timetuple())
        else:
            start_datetime = time.mktime(datetime(2012, 1, 1, 0, 0).timetuple())
        end_datetime = time.mktime(datetime(datetime.now().year, datetime.now().month, datetime.now().day,
                                            datetime.now().hour, datetime.now().minute)
                                   .timetuple())

        # Get the prices, market_cap and volumes from coinGecko
        response = CoinGeckoAPI().get_coin_market_chart_range_by_id(coin_id, 'usd', start_datetime, end_datetime)

        # Create the prices Dataframe with the formatted timestamp (Coingecko returns 13 digit unix timestamp)
        prices_df = pd.DataFrame.from_dict(response['prices'])
        prices_df.columns = ['timestamp', 'price']
        prices_df.set_index('timestamp')
        prices_df['coin'] = coin_id

        # Create the market cap Dataframe with the formatted timestamp (Coingecko returns 13 digit unix timestamp)
        market_cap_df = pd.DataFrame.from_dict(response['market_caps'])
        market_cap_df.columns = ['timestamp', 'market cap']
        market_cap_df.set_index('timestamp')

        # Create the prices volume Dataframe with the formatted timestamp (Coingecko returns 13 digit unix timestamp)
        volume_df = pd.DataFrame.from_dict(response['total_volumes'])
        volume_df.columns = ['timestamp', 'volume']
        volume_df.set_index('timestamp')

        # Create the combined Dataframe with the formatted timestamp (Coingecko returns 13 digit unix timestamp)
        combined_df = prices_df.merge(market_cap_df, how='left', on='timestamp').merge(volume_df, how='left',
                                                                                       on='timestamp')
        combined_df['timestamp'] = pd.to_datetime(combined_df['timestamp'], unit='ms')
        combined_df.sort_values('timestamp')

        # Include the division between market cap and price and volume and price
        combined_df['market/price'] = combined_df['volume'] / combined_df['price']

        # include the difference of price between every timestamp (we include that difference in first day is 0)
        combined_df['price difference'] = combined_df['price'].diff()

        # include the percentage of the difference of price between every timestamp
        combined_df['price % difference'] = combined_df['price difference'] / combined_df['price'].shift(1) * 100

        # Return the response
        return combined_df

    @staticmethod
    def get_coin_list():
        print('Calling the getAllCoins function')
        response = CoinGeckoAPI().get_coins_markets('usd', per_page=250, price_change_percentage='24h', page=1)
        return_df = pd.DataFrame.from_dict(response)
        x = 1
        print('X is equal to: ' + str(x) + ' Length of the list is: ' + str(len(return_df)))
        while len(response) != 0:
            x = x + 1
            response = CoinGeckoAPI().get_coins_markets('usd', per_page=250, price_change_percentage='24h', page=x)
            return_df = pd.concat([return_df, pd.DataFrame.from_dict(response)], ignore_index=True)
            print('X is equal to: ' + str(x) + ' Length of the list is: ' + str(len(return_df))
                  + ' response len: ' + str(len(response)))
        return return_df

