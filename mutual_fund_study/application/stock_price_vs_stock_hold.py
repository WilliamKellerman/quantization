import tushare as ts
import datetime
import pandas as pd
import plot_utility
import single_fund_stock_hold


# 获取单只基金的所有历史持仓股票 "基金持仓 vs 股价" 图
def get_stock_price_vs_stock_hold_plot_by_series(fund_code: str, fund_name: str):
    start_date = '20100101'
    now = datetime.datetime.today().strftime('%Y%m%d')
    fund_df = single_fund_stock_hold.get_one_fund_all_season_stock_hold_vol_current_only(
        fund_code=fund_code, start_date=start_date, end_date=now)

    for index, row in fund_df.iterrows():
        stock_code = row['股票代码']
        stock_name = row['股票名称']

        # 加工股价数据 stock_price_s
        df_price = ts.pro_bar(ts_code=stock_code, adj='qfq', start_date=start_date, end_date=now, freq='M')
        if df_price is None:
            print(stock_code + stock_name + "：无行情数据")
            continue
        df_price.index = df_price.apply(lambda r: datetime.datetime.strptime(r['trade_date'], '%Y%m%d').date(),
                                        axis='columns')
        df_price.sort_index(inplace=True)
        stock_price_s = df_price['close']
        stock_vol_s = df_price['vol']

        # 加工基金持仓数据 stock_hold_s
        row = row.copy()
        row.drop(labels=['股票代码', '股票名称'], inplace=True)
        stock_hold_df = pd.DataFrame({'持仓': row})
        stock_hold_df['格式日期'] = stock_hold_df.index
        stock_hold_df.index = stock_hold_df.apply(lambda r: datetime.datetime.strptime(r['格式日期'], '%Y%m%d').date(),
                                                  axis='columns')
        stock_hold_s = stock_hold_df['持仓']
        stock_hold_s.fillna(0.0, inplace=True)

        # 画图
        plot_utility.plot_3_series_in_one_figure(s_l=stock_price_s, s_r=stock_hold_s, s_low=stock_vol_s,
                                                 title=fund_name + '---' + stock_name + '[' + stock_code + ']',
                                                 x_label='日期', y_label_l='股价(元)', y_label_r='基金持仓(股)',
                                                 y_label_low='成交量(股)',
                                                 sub_folder_name=fund_name)


# 获取单只基金的所有历史持仓股票 "基金持仓 vs 股价k线" 图
def get_stock_price_kline_vs_stock_hold_plot(fund_code: str, fund_name: str):
    start_date = '20200101'
    now = datetime.datetime.today().strftime('%Y%m%d')
    fund_df = single_fund_stock_hold.get_one_fund_all_season_stock_hold_vol_current_only(
        fund_code=fund_code, start_date=start_date, end_date=now)

    for index, row in fund_df.iterrows():
        stock_code = row['股票代码']
        stock_name = row['股票名称']

        # 加工股价数据 df_price
        df_price = ts.pro_bar(ts_code=stock_code, adj='qfq', start_date=start_date, end_date=now, freq='M')
        if df_price is None:
            print(stock_code + stock_name + "：无行情数据")
            continue
        df_price.drop(columns=['ts_code', 'pre_close', 'change', 'pct_chg', 'amount'], inplace=True)
        df_price.columns = ['trade_date', 'close', 'open', 'high', 'low', 'volume']
        df_price['日期'] = df_price.apply(lambda r: datetime.datetime.strptime(r['trade_date'], '%Y%m%d'), axis='columns')

        # 加工基金持仓数据 df_stock_hold
        row = row.copy()
        row.drop(labels=['股票代码', '股票名称'], inplace=True)
        stock_hold_df = pd.DataFrame({'持仓': row})
        stock_hold_df = stock_hold_df.rename(index=pd.Timestamp)
        stock_hold_s = stock_hold_df['持仓']
        stock_hold_s.fillna(0.0, inplace=True)
        stock_hold_s = stock_hold_s.resample('D').asfreq().interpolate()
        df_stock_hold = pd.DataFrame({'持仓': stock_hold_s, '日期': stock_hold_s.index})
        df_stock_hold = df_stock_hold.reset_index()

        # 将持仓拟合日线 与 股价月线 merge
        df_merge = df_price.merge(df_stock_hold, how='left', on='日期')
        df_merge.index = df_merge['日期']
        df_merge = df_merge.rename(index=pd.Timestamp)
        df_merge = df_merge.sort_index(ascending=True)
        series_hold = df_merge['持仓']
        series_hold = series_hold.sort_index(ascending=True)

        # 画图
        plot_utility.plot_kline_with_hold(s_hold=series_hold, df_price=df_merge,
                                          title=fund_name + '---' + stock_name + '[' + stock_code + ']',
                                          y_label='价格', y_label_lower='成交量')


# 获取基金维度的平均持股周期
def get_stock_price_vs_stock_hold_from_fund_list():
    fund_list = [
        # ('169101.OF', '东证睿丰'),
        # ('007119.OF', '睿远成长价值A'),
        # ('008969.OF', '睿远均衡价值A'),
        # ('001112.OF', '东方红中国优势'),
        # ('001985.OF', '富国低碳新经济A'),
        # ('002803.OF', '东方红沪港深'),
        # ('501049.OF', '东方红睿玺'),
        # ('169102.OF', '东方红睿阳'),
        # ('501054.OF', '东方红睿泽'),
        # ('004424.OF', '汇添富文体娱乐主'),
        # ('005028.OF', '鹏华研究精选'),
        # ('005450.OF', '华夏稳盛'),
        # ('005827.OF', '易方达蓝筹精选'),
        # ('006408.OF', '汇添富消费升级'),
        # ('006551.OF', '中庚价值领航'),
        # ('007044.OF', '博道沪深300指数增A'),
        # ('007412.OF', '景顺长城绩优成长'),
        # ('008063.OF', '汇添富大盘核心资产'),
        # ('008286.OF', '易方达研究精选'),
        # ('008294.OF', '朱雀企业优胜A'),
        # ('008314.OF', '上投摩根慧选成长A'),
        # ('008545.OF', '泓德丰润三年持有'),
        # ('008969.OF', '睿远均衡价值三年A'),
        # ('009138.OF', '嘉实瑞成两年持有期'),
        # ('009576.OF', '东方红智远三年持有'),
        # ('163406.OF', '兴全合润'),
        # ('519066.OF', '汇添富蓝筹稳健'),
        # ('001725.OF', '汇添富高端制造证券投资基金'),
        # ('005802.OF', '汇添富智能制造股票证券投资基金'),
        # ('320007.OF', '诺安成长混合'),
        ('004997.OF', '广发高端制造A'),

    ]

    df_base = pd.DataFrame(data=fund_list, columns=['基金代码', '基金名称'])
    df_base.apply(lambda row: get_stock_price_vs_stock_hold_plot_by_series(row['基金代码'], row['基金名称']), axis='columns')


# get_stock_price_kline_vs_stock_hold_plot('169101.OF', '东证睿丰')
get_stock_price_vs_stock_hold_from_fund_list()
# get_stock_price_vs_stock_hold_plot_by_series('169101.OF', '东证睿丰')
print('end')
