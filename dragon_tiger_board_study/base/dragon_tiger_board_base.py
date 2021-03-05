import tushare as ts
import datetime
from customize_exception import CustomizeException


# 初始化公共资源
ts.set_token('4815a591b35b6008893f76680efc01b000929579b688ad33449d9888')
pro = ts.pro_api()

# 定义龙虎榜接口字典
dragon_tiger_board_dict = {'交易日期': 'trade_date', 'TS代码': 'ts_code', '营业部名称': 'exalter', '买入额': 'buy',
                           '买入占总成交比例': 'buy_rate', '卖出额': 'sell', '卖出占总成交比例': 'sell_rate', '净成交额': 'net_buy'}


# 龙虎榜数据接口基类
class DragonTigerBoardBase:

    def __init__(self, date):
        self.date = date

        # 初始化元素默认值
        self.order_type = dragon_tiger_board_dict['净成交额']
        self.filter_type = dragon_tiger_board_dict['营业部名称']
        self.filter = '机构专用'
        self.num = 3

    def get_top_inst_ts_code(self):
        df = pro.top_inst(trade_date=self.date).drop_duplicates()

        # 进行过滤，过滤字段可选 过滤内容可自定义
        df = df[df[self.filter_type] == self.filter]

        # 根据ts_code聚合，排序类别可选，排序后选取股票数量可自定义
        df_new = df.groupby('ts_code').sum().sort_values(self.order_type, ascending=False).head(self.num)

        return df_new.index


# 交易日列表基类
class TradeDateBase:

    def __init__(self, date):
        self.date = date

        # 初始化元素默认值
        self.day_num = 2    # 从起始日开始获取交易日个数

    def __get_trade_date_list_df(self):
        now = datetime.datetime.today().strftime('%Y%m%d')
        date_df = pro.trade_cal(start_date=self.date, end_date=now)

        # 仅获取交易日
        trade_date_df = date_df[date_df['is_open'] == 1]

        return trade_date_df

    def get_trade_date_list_by_num(self):
        trade_date_df = self.__get_trade_date_list_df()

        if len(trade_date_df) < self.day_num:
            raise CustomizeException(None, '查询起始日到今日不足自定义查询天数')

        date_list = []
        i = 0
        for index, row in trade_date_df.iterrows():
            if i == self.day_num:
                break
            i = i + 1
            date_list.append(row['cal_date'])

        return date_list
