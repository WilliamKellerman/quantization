import pandas as pd
import numpy as np

# 布尔运算
val = np.arange(10, 60).reshape(10, 5)
col = ["ax", "bx", "cx", "dx", "ex"]
idx = list("abcdefghij")
df1 = pd.DataFrame(val, columns = col, index = idx)
print("dataframe", "*" * 11)
print(df1)
print("*" * 21, "<- dataframe")
bs = df1["bx"] > 30

print("bs:", "*" * 11)
print(bs)

print("filtered df", "*" * 11)
df2 = df1[bs]
print(df2)


# 手动建立一个filter series
v = [False, False, False, False, False, True, True, True, True, True]
bs_manual = pd.Series(v, index=idx)
df3 = df1[bs_manual]
print(df3)
print("end")
