import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tushare as ts
import datetime
import fund_charactor_study

date1 = np.arange(start=0.01, stop=np.e, step=0.01)
date2 = np.arange(start=0.01, stop=np.e, step=0.5)
price = np.exp(date1)
vol = np.log(date2)


def plot_2_series_in_same_figure(x1, y1, x2, y2):
    fig = plt.figure()

    # add_subplot(1, 1, 1) 意思：建立划分1行1列的子图，取第1幅子图
    ax1 = fig.add_subplot(1, 1, 1)
    ax1.plot(x1, y1)
    ax1.set_ylabel('Y values for exp(-x)')
    ax1.set_title("Double Y axis")
    ax1.set_xlabel('Same X for both exp(-x) and ln(x)...1')

    ax2 = ax1.twinx()  # 两组数列画在同一张图的关键
    ax2.plot(x2, y2, 'r')
    ax2.set_xlim([0, np.e])
    ax2.set_ylabel('Y values for ln(x)')
    ax2.set_xlabel('Same X for both exp(-x) and ln(x)...2')  # 实测发现本行不起作用

    plt.show()
    plt.savefig('./this_is_a_plot.png')


def point_df_test():
    start_date = '20100101'
    now = datetime.datetime.today().strftime('%Y%m%d')
    df_price = ts.pro_bar(ts_code='601318.SH', adj='qfq', start_date=start_date, end_date=now, freq='M')
    stock_price_df = df_price[['trade_date', 'close']]
    stock_price_df = stock_price_df.copy()
    stock_price_df['date'] = stock_price_df.apply(
        lambda r: datetime.datetime.strptime(r['trade_date'], '%Y%m%d').date(), axis='columns')
    stock_price_df = stock_price_df[['date', 'close']]

    ax = stock_price_df.plot(x='date')
    # df_2.plot(ax=ax, secondary_y=True)

    ax.figure.autofmt_xdate()

    plt.show()

    print('end')


plot_2_series_in_same_figure(x1=date1, y1=price, x2=date2, y2=vol)
# point_df_test()

print('end')
