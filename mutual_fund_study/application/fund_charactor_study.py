from utility import dataFrame_utility
import pandas as pd
import numpy as np
import datetime
import single_fund_stock_hold


"""
通过查询基金成立以来各个季度报告期的重仓，研究基金的调性，例如：持股周期均值，最大值，最小值，方差
"""


# 获取单基金下所有持股的平均持股周期
def get_stock_hold_seasons_mean(fund_code: str, fund_name: str) -> pd.DataFrame:
    start_date = '20100101'
    now = datetime.datetime.today()
    all_season_df = single_fund_stock_hold.get_one_fund_all_season_stock_hold_vol(fund_code=fund_code, start_date=start_date, end_date=now)
    all_season_df_data_only = all_season_df.drop(columns=['股票代码', '股票名称'])
    season_count = all_season_df_data_only.shape[1]

    all_season_df['持股季度数'] = all_season_df_data_only.apply(dataFrame_utility.get_max_sub_series_length, axis='columns')

    stock_hold_seasons_mean = all_season_df['持股季度数'].mean()

    columns = ['基金代码', '基金名称', '基金存续期', '平均持股季度']
    data = np.array([fund_code, fund_name, season_count, stock_hold_seasons_mean]).reshape(1, 4)

    df_out = pd.DataFrame(data, columns=columns)

    return df_out


# 获取基金维度的平均持股周期
def get_fund_list_stock_hold_seasons_mean():
    fund_list = [
            ('007119.OF', '睿远成长价值A'),
            ('001112.OF', '东方红中国优势'),
            ('001985.OF', '富国低碳新经济A'),
            # ('002803.OF', '东方红沪港深'),
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
        ]

    df_base = pd.DataFrame(data=fund_list, columns=['基金代码', '基金名称'])
    df_list = []
    for index, row in df_base.iterrows():
        df = get_stock_hold_seasons_mean(row['基金代码'], row['基金名称'])
        df_list.append(df)

    df_final = pd.concat(df_list)
    return df_final


get_fund_list_stock_hold_seasons_mean()
print('end')
