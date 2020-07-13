import pandas as pd
import numpy as np

# 布尔运算
val = np.arange(10, 60).reshape(10, 5)
col = ["ax", "bx", "cx", "dx", "ex"]
idx = list("abcdefghij")
df1 = pd.DataFrame(val, columns=col, index=idx)
print("dataframe", "*" * 11)
print(df1)
print("*" * 21, "<- dataframe")


def single_func(data):
    return data * 2


df2 = df1.ax.map(single_func)


def dual_func(data):
    return data * 2, data * 3


df3 = df1.ax.map(dual_func)

df4 = df3.to_frame()


# for 循环
for i, row in df1.iterrows():
    row['ax2'] = row.ax * 2
    row['ax3'] = row.ax * 3

for i, row in df1.iterrows():
    df1.at[i, 'ax2'] = row.ax * 2
    df1.at[i, 'ax3'] = row.ax * 3


print(df1)

print('end')
