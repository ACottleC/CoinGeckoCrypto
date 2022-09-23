import pandas as pd
import os


class Utilities:
    @staticmethod
    def export_excel(dataframe, file_name):
        dataframe.to_excel('data/' + file_name + '.xlsx', index=False)

