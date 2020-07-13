import mpl_finance
import tushare as ts
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.pylab import date2num
import datetime

sns.set()
pro = ts.pro_api()

# 设置token，token为tushare网站注册时得到
ts.set_token('4815a591b35b6008893f76680efc01b000929579b688ad33449d9888')
# 获取pro_api
pro = ts.pro_api()


def get_stock_list_mock():
    """
    获取全量股票列表（前复权）Mock
    :return: full_stock_df, DataFrame
    """

    df = pd.DataFrame(
        [
            ['000001.SZ', '000001', '平安银行', '深圳', '银行', '19910403'],
            ['000002.SZ', '000002', '万科A', '深圳', '全国地产', '19910129'],
            ['000003.SZ', '000003', '国农科技', '深圳', '生物制药', '19910114'],
            ['000004.SZ', '000004', '世纪星源', '深圳', '房产服务', '20200810'],
            ['000005.SZ', '000005', '深振业A', '深圳', '区域地产', '20200627']
        ],
        columns=('ts_code', 'symbol', 'name', 'area', 'industry', 'list_date')
    )
    return df


def is_new_stock(list_date):
    """
    是否为新股
    :param list_date:
    :return:
    """
    today = datetime.date.today()

    list_date = datetime.datetime.strptime(list_date, '%Y%m%d').date()
    if today < (list_date + datetime.timedelta(days=30)):
        return True
    else:
        return False


def is_not_new_stock(list_date):
    """
    是否为非新股
    :param list_date:
    :return:
    """
    return not is_new_stock(list_date)


#
# def get_stock_list():
#     """
#     获取全量股票列表（前复权）
#     :return: df, DataFrame
#     """
#     # tushare识别码，股票代码，名称，概念，行业，上市时间
#     df = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
#
#     not_new_df = df[df.list_date.map(not is_new_stock)]
#     return not_new_df
#
#
# # 生成时间范围
# def init_day_range(days):
#     """
#     生成时间范围
#     :param days: Int
#     :return: Tuple
#     """
#     today = datetime.date.today()
#     today = today.strftime('%Y%m%d')
#
#     days_ago = datetime.date.today() - datetime.timedelta(days=days)
#     days_ago = days_ago.strftime('%Y%m%d')
#
#     return days_ago, today
#
#
# def cal_stock_vol_rate(ts_code):
#     """
#     计算成交量比率
#     :param ts_code: '600958.SH', String
#     :return: vol_rate, Float
#     """
#     days_ago, today = init_day_range(30)
#
#     single_stock_df = ts.pro_bar(ts_code=ts_code, adj='qfq', start_date=days_ago, end_date=today)
#
#     # 通过 pct_chg 涨幅的正负，判断 volume 的方向
#     # 涨子集
#     single_stock_df_pos = single_stock_df[single_stock_df.pct_chg > 0]
#     vol_sum_pos = single_stock_df_pos.vol.sum()
#
#     # 跌子集
#     single_stock_df_neg = single_stock_df[single_stock_df.pct_chg < 0]
#     vol_sum_neg = single_stock_df_neg.vol.sum()
#
#     if vol_sum_neg > 1e-3:
#         vol_rate = vol_sum_pos / vol_sum_neg
#     else:
#         vol_rate = 9999
#
#     return vol_rate
#
#
# def print_to_excel(df):
#     """
#     打印到文件
#     :param df:
#     :return:
#     """
#     today = datetime.date.today()
#     today = today.strftime('%Y-%m-%d')
#     # filename = '~/Downloads/' + today + '.xls'
#     filename = today + '.xls'
#     df.to_excel(excel_writer=filename, sheet_name='11')
#
#

full_stock_df = get_stock_list_mock()

bs = full_stock_df.list_date

bs1 = bs.map(is_not_new_stock)

not_new_df = full_stock_df[bs1]

#
# full_stock_df['vol_rate'] = full_stock_df.ts_code.map(cal_stock_vol_rate)
#
# full_stock_df.sort_values('vol_rate', inplace=True, ascending=False)
#
# print_to_excel(full_stock_df)
#
print("end")
