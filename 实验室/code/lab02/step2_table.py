import pandas as pd

df = pd.DataFrame({
    "region":   ["华东", "华东", "华北", "华北", "华南", "华南", "华东"],
    "category": ["纸品", "文具", "纸品", "文具", "纸品", "文具", "文具"],
    "amount":   [120, 80, 200, 60, 150, 90, 110],
    "orders":   [3, 2, 4, 1, 5, 3, 2],
})

print("原始表:")
print(df)

print("\n每个大区的总额:")
print(df.groupby("region")["amount"].sum())

print("\n每个品类的平均金额:")
print(df.groupby("category")["amount"].mean().round(1))

df["per_order"] = df["amount"] / df["orders"]
print("\n各大区客单价(总额 / 总单数):")
print((df.groupby("region")["amount"].sum() / df.groupby("region")["orders"].sum()).round(1))
