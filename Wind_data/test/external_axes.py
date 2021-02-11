import pandas as pd
import mplfinance as mpf
import matplotlib.dates as mdates

idf = pd.read_csv('data/SPY_20110701_20120630_Bollinger.csv', index_col=0, parse_dates=True)
idf.shape
idf.head(3)
idf.tail(3)
df = idf   #.loc['2011-07-01':'2011-12-30', :]

fig = mpf.figure(style='yahoo', figsize=(7, 8))
ax1 = fig.add_subplot(2, 1, 1)
ax2 = fig.add_subplot(2, 1, 2)

mpf.plot(df, ax=ax1, volume=ax2)

# 修改刻度定位器
year_locator = mdates.YearLocator(month=12, day=31)  # 每年最后一天
season_locator = mdates.MonthLocator(bymonth=[3, 6, 9, 12], bymonthday=-1)  # 每季度最后一天
month_locator = mdates.MonthLocator()

ax1.xaxis.set_major_locator(season_locator)
ax1.xaxis.set_minor_locator(month_locator)
ax1.grid(which='major', color='red', ls='-.')
ax1.grid(which='minor', color='orangered', linewidth=0.25, ls='-.')
# ax1.figure.autofmt_xdate()

ax2.xaxis.set_major_locator(season_locator)
ax2.xaxis.set_minor_locator(month_locator)
ax2.grid(which='major', color='red', ls='-.')
ax2.grid(which='minor', color='orangered', linewidth=0.25, ls='-.')
# ax2.figure.autofmt_xdate()

# mpf.show()

print('end')
