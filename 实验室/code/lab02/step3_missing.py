import pandas as pd
import numpy as np

df = pd.DataFrame({
    "name":  ["a", "b", "c", "d"],
    "score": [90, np.nan, 70, np.nan],
})

print(df)
print("\ncount(非空个数) =", df["score"].count())
print("mean(平均)       =", df["score"].mean())
print("sum(求和)        =", df["score"].sum())
print("\n如果把缺失当 0 来算,平均会变成:", df["score"].fillna(0).mean())
print("缺失情况:")
print(df.isna().sum())
