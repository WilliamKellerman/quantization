import mplfinance as mpf
import tushare as ts
import pandas as pd
import datetime
import matplotlib.pyplot as plt

# 设置token，token为tushare网站注册时得到
ts.set_token('4815a591b35b6008893f76680efc01b000929579b688ad33449d9888')


def get_stock_price_df(stock_code: str, start_date: str, end_date: str, freq='M') -> pd.DataFrame:
    price_df = ts.pro_bar(ts_code=stock_code, adj='qfq', start_date=start_date, end_date=end_date, freq=freq)
    # price_df = pro.price_df(ts_code='600958.SH', start_date='20200101', end_date='20210130')

    price_df.info()
    # 其中的open、high、low、close、和vol几列信息是我们需要的，其余的数据列都可以删除掉，
    # 另外，这些数据的Index并不是时间序列，交易日期是以字符串的形式存储在trade_date列中的，
    # 需要将日期作为DataFrame的Index，并把它们转化为pandas.Timestamp格式。
    price_df.index = price_df.trade_date
    price_df = price_df.rename(index=pd.Timestamp)
    price_df.drop(columns=['ts_code', 'trade_date', 'pre_close', 'change', 'pct_chg', 'amount'], inplace=True)
    price_df.columns = ['close', 'open', 'high', 'low', 'volume']
    price_df.sort_index(inplace=True)
    price_df.info()
    return price_df


# TODO: WANGHANBO 通过 mpf.make_addplot 将基金持仓数据画入图中，验证：
#  两个DF的X轴数据密度不一致，能否画？(实测不能，可否变通)
#  终极解决方案：通过数据插值方式，将持仓量插值到每个月一个点
# 参考 https://qdhhkj.blog.csdn.net/article/details/105783640
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.resample.html
# 数据变频，聚合与插值 https://blog.csdn.net/starter_____/article/details/81437626
def add_plot_test():
    now = datetime.datetime.today().strftime('%Y%m%d')
    df_1 = get_stock_price_df(stock_code='600958.SH', start_date='20160101', end_date=now)
    df_2 = get_stock_price_df(stock_code='601398.SH', start_date='20160101', end_date=now)

    add_plot = mpf.make_addplot(df_2.volume, type='line', secondary_y='auto')
    mpf.plot(df_1, type='candle', volume=True, style='yahoo', addplot=add_plot)

    print('end')


# 试验发现，mplfinance画k线，
# show_nontrading=False 横轴只会简单依据数据点画图，当横轴的时间密度不一致时，也不会主动放缩调整。
# show_nontrading=True 当横轴的时间密度不一致时，不影响画图效果。
def df_concat_test():
    df_1 = get_stock_price_df(stock_code='600958.SH', start_date='20160101', end_date='20170101', freq='M')
    df_2 = get_stock_price_df(stock_code='600958.SH', start_date='20200101', end_date='20210101', freq='W')

    df = pd.concat([df_1, df_2])
    mpf.plot(df, type='candle', volume=True, style='yahoo', show_nontrading=True)

    print('end')


# TODO: CHAIFENG
#  1、通过 marketcolors 和 mpf_style，将K线画成符合中国特色的红涨绿跌的形式
#  参考 https://qdhhkj.blog.csdn.net/article/details/105783640
#  https://github.com/matplotlib/mplfinance/blob/master/examples/using_lines.ipynb
#  2、画网格：x major：年  minor：季度
def style_test():
    now = datetime.datetime.today().strftime('%Y%m%d')
    df_1 = get_stock_price_df(stock_code='002415.SZ', start_date='20160101', end_date=now)

    my_color = mpf.make_marketcolors(up='red', down='green', edge='inherit', wick='inherit', volume='inherit')
    my_style = mpf.make_mpf_style(marketcolors=my_color, gridaxis='both', gridstyle='-.', y_on_right=True)

    # fig = plt.figure()
    # 建立划分1行1列的子图，取第1幅子图
    # ax1 = fig.add_subplot(1, 1, 1)
    mpf.plot(df_1, type='candle', volume=True, figscale=1.5, style=my_style, title='****报价', figratio=(5, 5), ylabel='价格', ylabel_lower='成交量', savefig='my_image.png')

    print('end')


# add_plot_test()
# style_test()
df_concat_test()
print('end')
