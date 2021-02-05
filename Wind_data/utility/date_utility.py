import pandas as pd
import datetime


# 生成季度序列
def generate_season_date_list(start_date: str, end_date: str) -> list:
    dti = pd.date_range(start=start_date, end=end_date, freq='Q')
    date_list = dti.strftime('%Y%m%d').tolist()
    return date_list


# list [20200630, 20200930] -> str [20200630, 20200930]
def list_to_str(l):
    string = '[' + '，'.join(l) + ']'

    return string


# yyyyMMdd -> yyyy-MM-dd 格式自定义
def date_format_str_to_str(date_in: str, format_in: str, format_out: str) -> str:
    dt = datetime.datetime.strptime(date_in, format_in)
    date_out = dt.strftime(format_out)
    return date_out
