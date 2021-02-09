import datetime
import pandas as pd
import tushare as ts
import mplfinance as mpf
from scipy import interpolate
import numpy as np
import matplotlib.pyplot as plt

now = datetime.datetime.today().strftime('%Y%m%d')
hold = [1232123123, 23123123123, 32334234422, 12842928383, 44842928383, 26842928383]
hold_new = [1232123123, 23123123123, 32334234422, 12842928383, 43423423424, 23423522131,
            44842928383, 26842928383, 44842928382, 26842928383, 66842928383]
x = np.linspace(0, 10, 6)
x_new = np.linspace(0, 10, 11)

last = datetime.date(datetime.date.today().year, datetime.date.today().month, 1)-datetime.timedelta(1)
years = ['20190101', '20190301', '20190501', '20190701', '20191001', '20200101']
years_new = ['20190101', '20190201', '20190301', '20190401', '20190501', '20200601', '20190701',
             '20190801', '20190901', '20191101', '20200101']
pg_1 = pd.DataFrame({'持仓': hold, '日期': years})
pg_1.index = pg_1['日期']
pg_1 = pg_1.rename(index=pd.Timestamp)
pg_2 = pg_1['持仓']

pg_1_new = pd.DataFrame({'持仓': hold_new, '日期': years_new})
pg_1_new.index = pg_1_new['日期']
pg_1_new = pg_1_new.rename(index=pd.Timestamp)
pg_2_new = pg_1_new['持仓']
# f = interpolate.interp1d(pg_2.index, pg_2, kind='linear')
# pg_2_new = pd.DataFrame({'持仓': f(pg_2_new.index)})
# f函数计算时间报错
f = interpolate.interp1d(x, pg_2, kind='cubic')
pg_3_new = pd.DataFrame({'持仓': f(x_new)})
# interp1d 拟合的f函数 在 x_new 区间大于 x 时无法计算

pg_3_new.plot()

plt.show()
# series_m = pg_2.resample('M').asfreq().interpolate()

# price_df = ts.pro_bar(ts_code='600958.SH', adj='qfq', start_date='20200101', end_date=now, freq='M')
# price_df.index = price_df.trade_date
# price_df = price_df.rename(index=pd.Timestamp)
# price_df.drop(columns=['ts_code', 'trade_date', 'pre_close', 'change', 'pct_chg', 'amount'], inplace=True)
# price_df.columns = ['close', 'open', 'high', 'low', 'volume']
# price_df.sort_index(inplace=True)
# price_df.info()

# add_plot = mpf.make_addplot(series_m, type='line', secondary_y='auto')
# mpf.plot(price_df, type='candle', volume=True, style='yahoo', addplot=add_plot)

# 验证得出 X轴密度相同，数值不同可以画在一起
# 问题1：点位不完全正确
# 目前看起来X轴是由 plot 入参 df 确定， addplot 以现有的X轴按顺序画点      结论正确
# 问题2：目前只找到了向前插值，向后插值 api 暂时还没有找到均匀填充的方法
# 目前尝试出可行方案为通过 asfreq() 重采集后获得nan空位，再使用 interpolate() 线性填充，这个方案存在问题，重采集点位固定，如果原数据不在重采集点位内，则会被丢弃。

print('end')
