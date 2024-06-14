import pandas as pd
import json

# 读取JSON文件
with open("category_dict.json", "r") as file:
    category_dict = json.load(file)

# pathbase = r"D:/aaaStudy/MathModel_Optimization/Project/2023C"
# ../ can get to father folder!

df = pd.read_excel("../Preprocess/按日分组.xlsx")
df["YearMonthDay"] = pd.to_datetime(df["YearMonthDay"])
df_filtered = df[
    (df["YearMonthDay"].dt.month == 6)
    & (df["YearMonthDay"].dt.day >= 24)
].T.iloc[1:, :]
# print(df_filtered.head())

df_filtered["sales"] = df_filtered.sum(axis=1)

df_filtered['max_sale'] = df_filtered.max(axis=1)

df_filtered["category"] = df_filtered.index.map(category_dict)

df_grouped = df_filtered.groupby("category").sum()
sales_dict = df_grouped.to_dict()["sales"]

df_filtered["sales_category"] = df_filtered["category"].map(sales_dict)
df_filtered["weight"] = df_filtered["sales"] / df_filtered["sales_category"]
print(df_filtered.head())
test = df_filtered.groupby("category").sum()

# print(test)

# df_filtered[['category', 'weight']].to_excel('weights.xlsx', index=True)

df_filtered = df_filtered[["category", "weight", "sales", "max_sale"]]
print(df_filtered.head())

df_grouped = df_filtered.groupby("category")

# for name, group in df_grouped:
#     temp = group[group["sales"] > 2.5]
#     print(name)
#     print(temp.shape[0] / group.shape[0])

df_filtered["available"] = ~(df_filtered["max_sale"] < 2.5)
df_filtered[["category", "weight", "available"]].to_excel("weights.xlsx", index=True)

df = pd.read_excel("../Preprocess/goods_ij.xlsx")
df_filtered["单品名称"] = df_filtered.index
df = df.merge(
    df_filtered[["单品名称", "weight", "available"]], how="left", on="单品名称"
)

df["weight"] = df["weight"].fillna(0)
df["available"] = df["available"].fillna(False)

true_count = df[df["available"] == True].shape[0]
print("Number of True rows:", true_count)

df.to_excel("goods_ij_weight_new.xlsx", index=False)
