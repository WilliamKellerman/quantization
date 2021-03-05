import tushare as ts
import datetime
from customize_exception import CustomizeException

# 设置token，token为tushare网站注册时得到
ts.set_token('4815a591b35b6008893f76680efc01b000929579b688ad33449d9888')

# 获取pro_api
pro = ts.pro_api()


def test_one_stock_top_inst_data():
    df = pro.top_inst(trade_date='20210303')

    df = df[df['ts_code'] == '000007.SZ'].sort_values('exalter', ascending=False)

    print(df)


def test_one_trade_date_top_three_code(date):
    df = pro.top_inst(trade_date=date).drop_duplicates()

    df = df[df['exalter'] == '机构专用']

    df_new = df.groupby('ts_code').sum().sort_values('net_buy', ascending=False).head(3)
    # df_new = df.groupby('ts_code').sum().sort_values('buy_rate', ascending=False).head(3)

    return df_new.index


def get_last_two_trade_date(date):
    now = datetime.datetime.today().strftime('%Y%m%d')
    date_df = pro.trade_cal(start_date=date, end_date=now)
    trade_date_df = date_df[date_df['is_open'] == 1].head(3)

    date_list = []
    for index, row in trade_date_df.iterrows():
        date_list.append(row['cal_date'])

    if len(date_list) < 3:
        raise CustomizeException(None, '查询日期到今日不足两个交易日')

    trade_date_list = [date_list[1], date_list[2]]
    return trade_date_list


def test_top_inst_last_two_trade_date():
    date = '20210301'
    trade_date_list = get_last_two_trade_date(date)

    last_one_day = trade_date_list[0]
    last_two_day = trade_date_list[1]
    code_list = test_one_trade_date_top_three_code(date)

    for code in code_list:
        price_df = ts.pro_bar(ts_code=code, adj='qfq', start_date=last_one_day, end_date=last_two_day, freq='D')
        open_t2 = price_df[price_df['trade_date'] == last_two_day]['open']
        open_t1 = price_df[price_df['trade_date'] == last_one_day]['open']
        open_different = open_t2.iloc[0] - open_t1.iloc[0]
        print('股票代码：[' + code + '], T+2开盘价 - T+1开盘价：[%.4f' % open_different + ']')


test_top_inst_last_two_trade_date()
