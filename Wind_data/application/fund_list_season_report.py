import excel_utility
from utility import excel_utility
from wind_api import wind_base_api
import pandas as pd

"""
通过wind，抓取基金当季度'重仓持股'
分析若干优选基金本季度与上季度的重仓变动
可以得到：
1、基金季度报告
2、股票维度的多空意见参考
"""


def get_branch1_fund_list():
    fund_list = [
        ('007119.OF', '睿远成长价值A'),
        ('001112.OF', '东方红中国优势'),
        ('001985.OF', '富国低碳新经济A'),
        # ('002803.OF', '东方红沪港深'),
        # ('004424.OF', '汇添富文体娱乐主)'),
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
    return fund_list


# 单只基金两季重仓
def get_one_fund_two_season_heavy_stock_hold(fund_code, fund_name, report_date_this_season, report_date_pre_season):
    single_fund_df_this_season = wind_base_api.get_one_fund_one_season_heavy_stock_hold(fund_code=fund_code,
                                                                                        report_date=report_date_this_season)
    single_fund_df_pre_season = wind_base_api.get_one_fund_one_season_heavy_stock_hold(fund_code=fund_code,
                                                                                       report_date=report_date_pre_season)

    single_fund_df_merged = pd.merge(left=single_fund_df_this_season, right=single_fund_df_pre_season,
                                     on=('股票代码', '股票名称'), how='outer',
                                     suffixes=('_当季', '_上季'),
                                     copy=True, indicator=False)

    # 填充 NaN
    single_fund_df_merged['所属行业'] = single_fund_df_merged['所属行业_当季'].fillna(single_fund_df_merged['所属行业_上季'])
    single_fund_df_merged.drop(columns=['所属行业_当季', '所属行业_上季'], inplace=True)
    single_fund_df_merged.fillna(0, inplace=True)

    # 增加两列基金信息
    assert isinstance(fund_code, str)
    single_fund_df_merged['基金代码'] = fund_code
    assert isinstance(fund_name, str)
    single_fund_df_merged['基金名称'] = fund_name
    # pd1 = pd.concat([s1, single_fund_hold])
    single_fund_df_merged['占基金净值比变动(%)'] = single_fund_df_merged.apply(
        lambda row: row['占基金净值比(%)_当季'] - row['占基金净值比(%)_上季'], axis='columns')

    return single_fund_df_merged


# 基金列表重仓(第一营业部精选)
def get_branch1_all_fund_heavy_stock_hold():
    fund_hold_list = []
    report_date_this_season = '20201231'
    report_date_pre_season = '20200930'
    fund_list = get_branch1_fund_list()
    for fund in fund_list:
        fund_code = fund[0]
        fund_name = fund[1]
        # 查询连续2季报表
        try:
            single_fund_hold = get_one_fund_two_season_heavy_stock_hold(fund_code=fund_code,
                                                                        fund_name=fund_name,
                                                                        report_date_this_season=report_date_this_season,
                                                                        report_date_pre_season=report_date_pre_season)

            fund_hold_list.append(single_fund_hold)
        except Exception:
            continue

    all_data_pd = pd.concat(fund_hold_list)
    excel_utility.append_to_new_sheet(all_data_pd, 'D:/demos/multi_sheet_output.xlsx',
                                      sheet_name='基金持仓变动')
    return


# 基金列表重仓(财富部大列表)
def get_caifu_all_fund_heavy_stock_hold():
    fund_hold_list = []
    report_date_this_season = '20201231'
    report_date_pre_season = '20200930'

    fund_df = excel_utility.read_caifu_2021_products_xls(file_path='./data/2021产品列表.xlsx')
    for index, row in fund_df.iterrows():
        fund_code = row['基金代码']
        fund_name = row['基金名称']
        # 查询连续2季报表
        try:
            single_fund_hold = get_one_fund_two_season_heavy_stock_hold(fund_code=fund_code,
                                                                        fund_name=fund_name,
                                                                        report_date_this_season=report_date_this_season,
                                                                        report_date_pre_season=report_date_pre_season)

            fund_hold_list.append(single_fund_hold)
        except Exception:
            continue
    all_data_pd = pd.concat(fund_hold_list)
    excel_utility.append_to_new_sheet(all_data_pd, './data/2021产品列表_结果.xlsx',
                                      sheet_name='基金持仓变动')
    return


get_caifu_all_fund_heavy_stock_hold()
print('end')
