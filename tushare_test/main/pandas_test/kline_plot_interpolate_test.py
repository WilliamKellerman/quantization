import datetime
import pandas as pd
import tushare as ts
import mplfinance as mpf
import numpy as np
from scipy import interpolate
import pylab as pl

# now = datetime.datetime.today().strftime('%Y%m%d')
# hold = [1232123123, 23123123123, 32334234422, 12842928383]
#
# last = datetime.date(datetime.date.today().year, datetime.date.today().month, 1)-datetime.timedelta(1)
# years = ['20190101', '20190501', '20191001', '20200131']
# pg_1 = pd.DataFrame({'持仓': hold, '日期': years})
# pg_1.index = pg_1['日期']
# pg_1 = pg_1.rename(index=pd.Timestamp)
# pg_2 = pg_1['持仓']
# # df_m = pg_2.resample('M').ffill()
#
# price_df = ts.pro_bar(ts_code='600958.SH', adj='qfq', start_date='20200101', end_date=now, freq='M')
# price_df.index = price_df.trade_date
# price_df = price_df.rename(index=pd.Timestamp)
# price_df.drop(columns=['ts_code', 'trade_date', 'pre_close', 'change', 'pct_chg', 'amount'], inplace=True)
# price_df.columns = ['close', 'open', 'high', 'low', 'volume']
# price_df.sort_index(inplace=True)
# price_df.info()
#
# add_plot = mpf.make_addplot(df_m, type='line', secondary_y='auto')
# mpf.plot(price_df, type='candle', volume=True, style='yahoo', addplot=add_plot, show_nontrading=True)

# 验证得出 X轴密度相同，数值不同可以画在一起
# 问题1：点位不完全正确
# 目前看起来X轴是由 plot 入参 df 确定， addplot 以现有的X轴按顺序画点      结论正确
# 问题2：目前只找到了向前插值，向后插值 api 暂时还没有找到均匀填充的方法

# -*-coding:utf-8 -*-


y = [1232123123, 23123123123, 32334234422, 12842928383]
x = ['20190101', '20190301', '20191201', '20200601']
start = pd.Timestamp('2019-01-01')
end = pd.Timestamp('2020-06-30')
xnew = pd.date_range(start='2019-01-01', end='2020-06-30', freq='M')
pl.plot(x, y, "ro")

for kind in ["nearest", "zero", "slinear", "quadratic", "cubic"]:  # 插值方式
    # "nearest","zero"为阶梯插值
    # slinear 线性插值
    # "quadratic","cubic" 为2阶、3阶B样条曲线插值
    f = interpolate.interp1d(x, y, kind=kind)
    # ‘slinear’, ‘quadratic’ and ‘cubic’ refer to a spline interpolation of first, second or third order)
    ynew = f(xnew)
    pl.plot(xnew, ynew, label=str(kind))
pl.legend(loc="lower right")
pl.show()

print('end')
