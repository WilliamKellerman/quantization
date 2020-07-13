import tushare as ts
import matplotlib.pyplot as plt

# 设置token，token为tushare网站注册时得到
ts.set_token('4815a591b35b6008893f76680efc01b000929579b688ad33449d9888')

# 获取pro_api
pro = ts.pro_api()

# 600958.SH，起始日期2020-01-01，结束日期2020-04-30日线数据
df = pro.daily(ts_code='600958.SH', start_date='20200101', end_date='20200430')

# 逆序后画图
df_rev = df.sort_index(ascending=False)  # 将DataFrame倒序
df_rev.plot(kind='line', x='trade_date', y='close', color='red', ylim=(0, 12), rot=45)  # 画图
plt.show()






# print(df['trade_date'], df(''))
print(df)