import numpy as np
import pandas as pd

"""
统计一行数据连续不是非数字的列总和
"""


def get_max_sub_series_length(s: pd.Series) -> int:
    max_sub = 0  # 最长子集长度
    count = 0  # 游标（临时存储长度）

    for i, r in s.iteritems():
        if not np.isnan(r):
            # 未找到nan，count++
            count = count + 1
        else:
            # 找到nan，更新 max_sub，复位 count
            if max_sub < count:
                max_sub = count
            count = 0
    max_sub = max_sub if max_sub > count else count
    return max_sub
