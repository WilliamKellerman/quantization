import mplfinance
import tushare as ts
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.pylab import date2num
import numpy as np

sns.set()
pro = ts.pro_api()

# 设置token，token为tushare网站注册时得到
ts.set_token('4815a591b35b6008893f76680efc01b000929579b688ad33449d9888')

# 获取pro_api
pro = ts.pro_api()

# 600958.SH，起始日期2020-01-01，结束日期2020-04-30日线数据
df = pro.daily(ts_code='600958.SH', start_date='20200101', end_date='20200130')

df = df.sort_values(by='trade_date', ascending=True)
df['trade_date2'] = df['trade_date'].copy()
df['trade_date'] = pd.to_datetime(df['trade_date']).map(date2num)
df['dates'] = np.arange(0, len(df))
df.head()


fig, ax = plt.subplots(figsize=(10, 5))
mplfinance.candles(
    ax=ax,
    quotes=df[['trade_date', 'open', 'close', 'high', 'low', 'volume']].values,
    width=0.7,
    colorup='r',
    colordown='g',
    alpha=0.7)
ax.xaxis_date()
plt.xticks(rotation=30)
plt.show()
