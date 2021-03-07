import tushare as ts
import matplotlib.pyplot as plt
import pandas as pd

# 设置token，token为tushare网站注册时得到
ts.set_token('4815a591b35b6008893f76680efc01b000929579b688ad33449d9888')

# 获取pro_api
pro = ts.pro_api()

# 600958.SH，起始日期20160101，结束日期20210101月线周线混合数据
df_1 = ts.pro_bar(ts_code='600958.SH', adj='qfq', start_date='20160101', end_date='20160301', freq='M')
df_2 = ts.pro_bar(ts_code='600958.SH', adj='qfq', start_date='20201201', end_date='20210101', freq='W')

df = pd.concat([df_1, df_2])

# 逆序后画图
df_rev = df.sort_values(by='trade_date', ascending=True)  # 将DataFrame倒序
df_rev.plot(kind='bar', x='trade_date', y='close', color='red', ylim=(0, 12), rot=15)  # 画图
plt.show()






# print(df['trade_date'], df(''))
print(df)