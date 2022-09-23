import pandas as pd
from os.path import exists
from DownloadFunctions import DownloadFunctions
from Utilities import Utilities
from datetime import datetime


print('Welcome to the CoinGecko App. Please select one of the following options:')
#We create an empty dictionary to store the dataframes that we have downloaded.
dictionary = dict()
#We get today's date in order to add to the files.
date_now = datetime.now().strftime('%Y-%m-%d')

#We launch the menu untill the user presses exit
ans = True
while ans:
    print('1) Get the historical price.\n'
          '2) Get the Information for the top Cryptocurrencies.\n'
          '7) Export all downloaded data. \n'
          '8) Exit Program.')
    ans = input('Please enter a number and hit enter.')
    if ans == '1':
        coin = input('Please enter the coin for which you want the historical price (e.g. bitcoin, ethereum, etc.)')
        print('Downloading historical prices for ' + coin + '.')
        dictionary['Prices_' + str(coin) + '_' + str(date_now)] = \
            DownloadFunctions().get_coin_prices(coin, '12/12/2020')
        print('Results have been downloaded. Here is a list of attributes that are included:\n'
              + str(dictionary.get('Prices_' + str(coin) + '_' + str(date_now)).columns.values))

    elif ans == '2':
        print('Information on top Cryptocurrencies.')

        # We check whether we have data for today downloaded or not (takes time to download the full report)
        if exists('data/CoinList_' + str(date_now) + '.xlsx') is False:
            print("The file for today doesn't exist so we download the data.")
            # We call the function get_all_coins
            dictionary['CoinList_' + str(date_now)] = DownloadFunctions().get_coin_list()

        else:

            re_download_data = ''
            while True:
                re_download_data = input('The file for today exists. Do you want to re download the data? Y/N. ')

                if re_download_data.lower() == 'y':
                    print('Re downloading the data, this might take a few minutes')
                    dictionary['CoinList_' + str(date_now)] = DownloadFunctions().get_coin_list()
                    break
                elif re_download_data.lower() == 'n':
                    print('Continuing with the already downloaded data, reading the file.')
                    dictionary['CoinList_' + str(date_now)] = pd.read_excel('data/CoinList_' + str(date_now) + '.xlsx')
                    break
                else:
                    print('Type Y/N')
    elif ans == '7':
        print('Exporting all the files that are available. The files will be stored in /data folder.')
        for key in dictionary:
            Utilities().export_excel(dictionary.get(key), key)
        print('All the files have been successfully exported.')
    elif ans == '8':
        print('Goodbye.')
        break
    else:
        print('Not Valid Choice Try again.')


print('End of program.')

