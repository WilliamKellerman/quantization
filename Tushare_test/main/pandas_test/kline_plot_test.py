import datetime
import pandas as pd
import tushare as ts
import mplfinance as mpf

now = datetime.datetime.today().strftime('%Y%m%d')
hold = [1232123123, 23123123123, 32334234422, 12842928383]

last = datetime.date(datetime.date.today().year, datetime.date.today().month, 1)-datetime.timedelta(1)
years = ['20200101', '20200501', '20201001', last]
pg_1 = pd.DataFrame({'持仓': hold, '日期': years})
pg_1.index = pg_1['日期']
pg_1 = pg_1.rename(index=pd.Timestamp)
pg_2 = pg_1['持仓']
df_m = pg_2.resample('M').ffill()

price_df = ts.pro_bar(ts_code='600958.SH', adj='qfq', start_date='20200101', end_date=now, freq='M')
price_df.index = price_df.trade_date
price_df = price_df.rename(index=pd.Timestamp)
price_df.drop(columns=['ts_code', 'trade_date', 'pre_close', 'change', 'pct_chg', 'amount'], inplace=True)
price_df.columns = ['close', 'open', 'high', 'low', 'volume']
price_df.sort_index(inplace=True)
price_df.info()

add_plot = mpf.make_addplot(df_m, type='line', secondary_y='auto')
mpf.plot(price_df, type='candle', volume=True, style='yahoo', addplot=add_plot)

# 验证得出 X轴密度相同，数值不同可以画在一起
# 问题1：点位不完全正确
# 目前看起来X轴是由 plot 入参 df 确定， addplot 以现有的X轴按顺序画点
# 问题2：目前只找到了向前插值，向后插值 api 暂时还没有找到均匀填充的方法

print('end')
