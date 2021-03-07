import tushare as ts
import datetime
from customize_exception import CustomizeException
import pandas as pd
from utility import excel_utility


# 设置token，token为tushare网站注册时得到
ts.set_token('4815a591b35b6008893f76680efc01b000929579b688ad33449d9888')

# 获取pro_api
pro = ts.pro_api()


# 获取起始日至今日交易日列表
def get_trade_date_list(start_date):
    now = datetime.datetime.today().strftime('%Y%m%d')
    date_df = pro.trade_cal(start_date=start_date, end_date=now)
    trade_date_df = date_df[date_df['is_open'] == 1]

    date_list = []
    for index, row in trade_date_df.iterrows():
        date_list.append(row['cal_date'])
    return date_list


# 获取起始日的后两个交易日
def get_last_two_trade_date(start_date):
    trade_date_list = get_trade_date_list(start_date)

    if len(trade_date_list) < 3:
        raise CustomizeException(None, '查询日期：[' + start_date + ']到今日不足两个交易日')

    two_trade_date_list = [trade_date_list[1], trade_date_list[2]]
    return two_trade_date_list


# 查询单日龙虎榜数据top3股票代码
def get_one_day_top_three_stock_code(date):
    # 去重
    df = pro.top_inst(trade_date=date).drop_duplicates()

    # 过滤出机构专用
    df = df[df['exalter'] == '机构专用']

    df_new = df.groupby('ts_code').sum().sort_values('net_buy', ascending=False).head(3)
    # df_new = df.groupby('ts_code').sum().sort_values('buy_rate', ascending=False).head(3)

    return df_new.index


# 查询两个交易日开盘价差值
def get_two_trade_date_open_difference(stock_code, date, trade_date_t1, trade_date_t2):
    price_df = ts.pro_bar(ts_code=stock_code, adj='qfq', start_date=trade_date_t1, end_date=trade_date_t2, freq='D')
    try:
        open_t2 = price_df[price_df['trade_date'] == trade_date_t2]['open'].iloc[0]
        open_t1 = price_df[price_df['trade_date'] == trade_date_t1]['open'].iloc[0]
    except IndexError as e:
        raise CustomizeException(None, '查询日期：[' + trade_date_t2 + ']尚未得到开盘价')

    open_different = open_t2 - open_t1
    open_info = {'stock_code': [stock_code], 'query_date': [date], 'open_t1': [open_t1], 'open_t2': [open_t2],
                 'open_different': [open_different]}
    open_info_df = pd.DataFrame(open_info)

    print('查询日期：[' + date + '], 股票代码：[' + stock_code + '], T+2开盘价 - T+1开盘价：[%.4f' % open_different + ']')
    return open_info_df


def get_history_open_difference():
    start_date = '20210101'
    # 获取交易日列表
    trade_date_list = get_trade_date_list(start_date)
    df_list = []

    for date in trade_date_list:
        # 查询单日龙虎榜数据top3股票代码列表
        code_list = get_one_day_top_three_stock_code(date)

        try:
            # 查询后两个交易日
            last_two_trade_date = get_last_two_trade_date(date)
            trade_date_t1 = last_two_trade_date[0]
            trade_date_t2 = last_two_trade_date[1]
        except CustomizeException as e:
            continue

        for code in code_list:
            try:
                open_info_df = get_two_trade_date_open_difference(code, date, trade_date_t1, trade_date_t2)
                df_list.append(open_info_df)
            except CustomizeException as e:
                continue

    all_data_pd = pd.concat(df_list)
    excel_utility.append_to_new_sheet(all_data_pd, 'D:/demos/multi_sheet_output.xlsx',
                                      sheet_name='t2开盘-t1开盘')
    print('end')


get_history_open_difference()
