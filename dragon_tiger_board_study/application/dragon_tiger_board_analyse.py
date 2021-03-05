import tushare as ts
from dragon_tiger_board_base import DragonTigerBoardBase, TradeDateBase, dragon_tiger_board_dict
import pandas as pd
from utility import excel_utility
from customize_exception import CustomizeException

# 设置token，token为tushare网站注册时得到
ts.set_token('4815a591b35b6008893f76680efc01b000929579b688ad33449d9888')
# 获取pro_api
pro = ts.pro_api()


def data_handle():
    query_date = '20210224'

    # 创建交易日基类实例
    trade_date_base = TradeDateBase(query_date)
    # 获取查询起始日到今天全部交易日列表
    trade_date_list = trade_date_base.get_trade_date_list_to_today()

    # 创建龙虎榜数据接口基类实例
    # 遍历交易日列表获取龙虎榜符合条件股票代码列表
    df_list = []
    for trade_date in trade_date_list:
        try:
            trade_date_zone = TradeDateBase(trade_date)
            trade_date_zone.day_num = 5
            # 获取自定义区间内交易日列表
            trade_date_list_by_num = trade_date_zone.get_trade_date_list_by_num()
        except CustomizeException as e:
            continue

        base = DragonTigerBoardBase(trade_date)
        # 自定义查询入参
        # base.num = 1
        # base.order_type = dragon_tiger_board_dict['买入占总成交比例']
        code_list = base.get_top_inst_ts_code()

        # 遍历股票代码列表获取行情数据
        for code in code_list:
            try:
                final_df = get_stock_price(code, trade_date, trade_date_list_by_num)
                df_list.append(final_df)
            except CustomizeException as e:
                continue

    all_data_pd = pd.concat(df_list)
    excel_utility.append_to_new_sheet(all_data_pd, 'D:/demos/dragon_tiger_data_output.xlsx',
                                      sheet_name='龙虎榜股票行情数据')
    print('end')


def get_stock_price(code, query_date, trade_date_list_by_num):
    # 获取起始日，结束日 用于查询行情
    begin_date = trade_date_list_by_num[0]
    end_date = trade_date_list_by_num[len(trade_date_list_by_num) - 1]

    df_price = ts.pro_bar(ts_code=code, adj='qfq', start_date=begin_date, end_date=end_date, freq='D')
    if df_price is None:
        print(code + "：无行情数据")

    stock_info = {'股票代码': [code], '查询日期': [query_date]}
    stock_info_df = pd.DataFrame(stock_info)
    try:
        counts = 0
        for trade_date in trade_date_list_by_num:
            if counts == len(trade_date_list_by_num):
                break
            counts = counts + 1
            df_price.copy()
            open = df_price[df_price['trade_date'] == trade_date]['open'].iloc[0]
            close = df_price[df_price['trade_date'] == trade_date]['close'].iloc[0]
            stock_info_df['t+' + str(counts) + '_开盘价'] = open
            stock_info_df['t+' + str(counts) + '_收盘价'] = close
    except IndexError as e:
        # 当日收盘前会出现该异常
        raise CustomizeException(None, '查询日期：[' + end_date + ']尚未得到该日行情信息')

    return stock_info_df


data_handle()

