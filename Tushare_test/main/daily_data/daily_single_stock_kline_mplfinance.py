import mplfinance as mpf
import tushare as ts
import pandas as pd
import datetime


# 设置token，token为tushare网站注册时得到
ts.set_token('4815a591b35b6008893f76680efc01b000929579b688ad33449d9888')


# 600958.SH，起始日期2020-01-01，结束日期2020-04-30日线数据
start_date = '20100101'
now = datetime.datetime.today().strftime('%Y%m%d')

daily = ts.pro_bar(ts_code='600958.SH', adj='qfq', start_date=start_date, end_date=now, freq='M')
# daily = pro.daily(ts_code='600958.SH', start_date='20200101', end_date='20210130')

daily.info()
# 其中的open、high、low、close、和vol几列信息是我们需要的，其余的数据列都可以删除掉，
# 另外，这些数据的Index并不是时间序列，交易日期是以字符串的形式存储在trade_date列中的，
# 需要将日期作为DataFrame的Index，并把它们转化为pandas.Timestamp格式。
daily.index = daily.trade_date
daily = daily.rename(index=pd.Timestamp)
daily.drop(columns=['ts_code', 'trade_date', 'pre_close', 'change', 'pct_chg', 'amount'], inplace=True)
daily.columns = ['open', 'high', 'low', 'close', 'volume']
daily.sort_index(inplace=True)
daily.info()

styles = mpf.available_styles()
styles = [
    # 'binance',
    # 'blueskies',
    # 'brasil',
    # 'charles',
    # 'checkers',
    # 'classic',
    # 'default',
    # 'mike',
    # 'nightclouds',
    # 'sas',
    # 'starsandstripes',
    'yahoo'
]

for style in styles:
    mpf.plot(daily, type='candle', volume=True, style=style)


# TODO: WANGHANBO 通过 mpf.make_addplot 将基金持仓数据画入图中，验证
#  1、两个DF的X轴数据密度不一致，能否画？
#  2、双Y轴，如果不是双Y轴，两个数据线的Y完全不在一个数量级上
# 参考 https://qdhhkj.blog.csdn.net/article/details/105783640

# TODO: CHAIFENG 通过 marketcolors 和 mpf_style，将K线画成符合中国特色的红涨绿跌的形式
# 参考 https://qdhhkj.blog.csdn.net/article/details/105783640

print('end')

