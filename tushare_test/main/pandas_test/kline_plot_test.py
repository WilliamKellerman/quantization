import datetime
import pandas as pd
import tushare as ts
import mplfinance as mpf
from scipy import interpolate
import numpy as np
import matplotlib.pyplot as plt


def test_interpolate():
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


def get_last_quarter(date_s):
    first_date = datetime.datetime.strptime(date_s[0], '%Y%m%d')
    quarter = (first_date.month - 1) / 3 + 1
    if quarter == 1:
        return datetime.datetime(first_date.year - 1, 12, 31).strftime('%Y%m%d')
    elif quarter == 2:
        return datetime.datetime(first_date.year, 3, 31).strftime('%Y%m%d')
    elif quarter == 3:
        return datetime.datetime(first_date.year, 6, 30).strftime('%Y%m%d')
    else:
        return datetime.datetime(first_date.year, 9, 30).strftime('%Y%m%d')


def test_merge_data_get_real_date():
    now = datetime.datetime.today().strftime('%Y%m%d')
    hold = [1232123123, 23123123123, 32334234422, 12842928383]

    last = datetime.date(datetime.date.today().year, datetime.date.today().month, 1) - datetime.timedelta(1)
    date = ['20200630', '20200531', '20201031', '20210131']
    pg_1 = pd.DataFrame({'持仓': hold, '日期': date})
    # 对起始日期上季度数据补0
    pg_1.sort_values(by='日期')
    date_s = pg_1['日期']
    date_need_supply = get_last_quarter(date_s)
    first_data = {'持仓': 0, '日期': date_need_supply}
    pg_1.append(first_data, ignore_index=True)

    pg_1.index = pg_1['日期']
    pg_1 = pg_1.rename(index=pd.Timestamp)
    pg_2 = pg_1['持仓']
    # TODO: 持仓左侧（或右侧）非0，拟合的函数有缺失，应保证左侧为0，右侧视情况
    # 已实现，日期列表起始点改为上季度最后一天，补数为0
    series_m = pg_2.resample('D').asfreq().interpolate()
    df_w = pd.DataFrame({'持仓': series_m})
    df_w = df_w.reset_index()

    price_df = ts.pro_bar(ts_code='600958.SH', adj='qfq', start_date='20150101', end_date=now, freq='M')
    price_df.drop(columns=['ts_code', 'pre_close', 'change', 'pct_chg', 'amount'], inplace=True)
    price_df.columns = ['trade_date', 'close', 'open', 'high', 'low', 'volume']
    price_df['日期'] = price_df.apply(lambda r: datetime.datetime.strptime(r['trade_date'], '%Y%m%d'), axis='columns')

    # TODO: 用 right join，仅保留每月线，
    #  理由1 日线都是拟合出来的，没有意义, 且占用存储
    #  理由2 price_DF, 持仓_DF, 数据时间跨度不一样，join之后，日线数据和月线数据混合，mplfinance画出的图只会简单数点，不缺分精度
    # 已实现
    df_new = price_df.merge(df_w, how='left', on='日期')
    # df_new = pd.merge(left=df_w, right=price_df, how='outer', on='日期')
    df_new.index = df_new['日期']
    df_new = df_new.rename(index=pd.Timestamp)
    df_new = df_new.sort_index(ascending=True)
    series_new = df_new['持仓']
    series_new.fillna(0.0, inplace=True)
    series_new = series_new.sort_index(ascending=True)
    add_plot = mpf.make_addplot(series_new, type='line', secondary_y='auto')
    mpf.plot(df_new, type='candle', volume=True, style='yahoo', addplot=add_plot)

    # 验证得出 X轴密度相同，数值不同可以画在一起
    # 问题1：点位不完全正确
    # 目前看起来X轴是由 plot 入参 df 确定， addplot 以现有的X轴按顺序画点      结论正确
    # 问题2：目前只找到了向前插值，向后插值 api 暂时还没有找到均匀填充的方法
    # 目前尝试出可行方案为通过 asfreq() 重采集后获得nan空位，再使用 interpolate() 线性填充，这个方案存在问题，重采集点位固定，如果原数据不在重采集点位内，则会被丢弃。


test_merge_data_get_real_date()

print('end')
