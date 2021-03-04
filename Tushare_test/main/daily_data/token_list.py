import tushare as ts
import matplotlib.pyplot as plt

# 设置token，token为tushare网站注册时得到
token_list = ['c80b73a45affc2ebbf9c19a72a1d9183de2a060a4569209dd58ef32e',  #方彬
              'c8a66e8744fe78f180baa4925b3e928456e75b9ef92908ea1be6810d',  #王永恒
              '33a4b73f97bd260f3a236c22c24cc5392871bb5e9f82cca6b0a95d1f',  #周雷雷
              '5cc777d657c7a4fb9ca7fa9c2b76d09879b01c92661438b0a8fb6b49',  #王剑峰
              '25a0a57951c2c60fd190d776c6baa3bdfbfef9dd324f28ebc0ec4230',  #柴丰
              '15784befcea92afbf00ce04480987b0b9918c7d371a254c3e7880990',  #刘琰
              '261254177312f03c178189cf6f019d4ac248df6559f3d4cd09d349c2',  #何彪
              ]

# 激活token为有效
for token in token_list:
    ts.set_token(token)

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