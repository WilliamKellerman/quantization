import pandas as pd
import numpy as np

val = np.arange(0, 30).reshape(10, 3)

# val = [('a1', 'b1', 'c1'), ('a2', 'b2', 'c2'), ('a3', 'b3', 'c3'), ('a4', 'b4', 'c4')]

idx = ["a", "b", "c"]
lbl = list("0123456789")
df = pd.DataFrame(val, columns=idx, index=lbl)

print(df)

filter_df = df.report_date = '202001031'

new_df = df[filter_df]

print('end')
