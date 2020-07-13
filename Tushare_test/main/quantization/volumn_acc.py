import tushare as ts
import pandas as pd
import seaborn as sns
import datetime

mock = False
# mock = True

sns.set()

# 设置token，token为tushare网站注册时得到
ts.set_token('4815a591b35b6008893f76680efc01b000929579b688ad33449d9888')
# 获取pro_api
pro = ts.pro_api()


def print_df(df, desc):
    """
    打印 DataFrame
    :param df: 目标
    :param desc: DataFrame描述
    :return:
    """
    print(desc, "*" * 21)
    print(df)
    print("*" * 21, '<-' + desc)


def get_stock_list_mock():
    """
    获取全量股票列表（前复权）Mock
    :return: full_stock_df, DataFrame
    """

    df = pd.DataFrame(
        [
            ['000001.SZ', '000001', '平安银行', '深圳', '银行', '19910403'],
            ['000002.SZ', '000002', '万科A', '深圳', '全国地产', '19910129'],
            ['000004.SZ', '000004', '国农科技', '深圳', '生物制药', '19910114'],
            ['000005.SZ', '000006', '世纪星源', '深圳', '房产服务', '20200810'],
            ['000006.SZ', '000006', '深振业A', '深圳', '区域地产', '20200627'],
            ['300156.SZ', '300156', '神雾环保', '北京', '环境保护', '20110107']
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
    if list_date is None:
        return False

    today = datetime.date.today()
    list_date = datetime.datetime.strptime(list_date, '%Y%m%d').date()

    # 如果今日日期< 上市日期+30日，则为新股
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


def get_stock_list():
    """
    获取全量股票列表（前复权）
    :return: df, DataFrame
    """
    if mock:
        return get_stock_list_mock()

    # tushare识别码，股票代码，名称，概念，行业，上市时间
    df = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
    return df


def init_day_range(days):
    """
    生成时间范围
    :param days: Int
    :return: Tuple
    """
    today = datetime.date.today()
    today = today.strftime('%Y%m%d')

    days_ago = datetime.date.today() - datetime.timedelta(days=days)
    days_ago = days_ago.strftime('%Y%m%d')

    return days_ago, today


def cal_stock_vol_rate(ts_code):
    """
    计算成交量比率
    :param ts_code: '600958.SH', String
    :return: price_rate, Float; vol_rate, Float
    """
    try:
        days_ago, today = init_day_range(30 * 3)

        # ts_code, trade_date, open, high, low, close, pre_close, change, pct_chg, vol, amount
        single_stock_df = ts.pro_bar(ts_code=ts_code, adj='qfq', start_date=days_ago, end_date=today)

        if single_stock_df is None:
            raise ValueError

        if single_stock_df.empty:
            raise ValueError

        max_price = single_stock_df.close.max()
        cur_price = single_stock_df.close[0]
        price_rate = cur_price / max_price

        # 通过 pct_chg 涨幅的正负，判断 volume 的方向
        # 涨子集
        single_stock_df_pos = single_stock_df[single_stock_df.pct_chg > 0]
        vol_sum_pos = single_stock_df_pos.vol.sum()

        # 跌子集
        single_stock_df_neg = single_stock_df[single_stock_df.pct_chg < 0]
        vol_sum_neg = single_stock_df_neg.vol.sum()

        vol_rate = vol_sum_pos / vol_sum_neg

        vol_price_rate = price_rate / vol_rate

    except BaseException as e:
        print("{0} has an exception: {1}".format(ts_code, e))
        return 9999, 9999, 9999, 9999, 9999, 9999, 9999
    else:
        return cur_price, max_price, price_rate, vol_sum_pos, vol_sum_neg, vol_rate, vol_price_rate


def print_to_excel(df):
    """
    打印到文件
    :param df:
    :return:
    """
    today = datetime.date.today()
    today = today.strftime('%Y-%m-%d')
    # filename = '~/Downloads/' + today + '.xls'
    filename = today + '.xls'
    if mock:
        filename = today + '-mock.xls'

    df.to_excel(excel_writer=filename, sheet_name='11')


FULL_STOCK_DF = get_stock_list()

# 打上新股标识
FULL_STOCK_DF['is_new'] = FULL_STOCK_DF.list_date.map(is_new_stock)

# 计算是否在高价位，阳量阴量比
for i, row in FULL_STOCK_DF.iterrows():
    tup = cal_stock_vol_rate(row.ts_code)
    FULL_STOCK_DF.at[i, 'cur_price'] = tup[0]
    FULL_STOCK_DF.at[i, 'max_price'] = tup[1]
    FULL_STOCK_DF.at[i, 'price_rate'] = tup[2]
    FULL_STOCK_DF.at[i, 'vol_sum_pos'] = tup[3]
    FULL_STOCK_DF.at[i, 'vol_sum_neg'] = tup[4]
    FULL_STOCK_DF.at[i, 'vol_rate'] = tup[5]
    FULL_STOCK_DF.at[i, 'vol_price_rate'] = tup[6]
    print('{0}-------->{1}'.format(str(i), tup))

# 按照阳量阴量比排序
FULL_STOCK_DF.sort_values('vol_price_rate', inplace=True, ascending=False)

print_to_excel(FULL_STOCK_DF)

print("end")
