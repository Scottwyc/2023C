import pandas as pd
import os
from openpyxl import load_workbook

# 读取数据
df = pd.read_excel("附件2.xlsx")
df["销售日期"] = pd.to_datetime(df["销售日期"])
df["年"] = df["销售日期"].dt.year

df["月"] = df["销售日期"].dt.month
df_grouped = df.groupby(["单品编码", "年", "月"])["销量(千克)"].sum().reset_index()
df_grouped = df_grouped.sort_values(["年", "月"])
df_grouped = df_grouped.pivot_table(
    index="单品编码", columns=["年", "月"], values="销量(千克)", fill_value=0
)
df_grouped.columns = [f"{year}-{month}" for year, month in df_grouped.columns]
df_grouped = df_grouped.loc[:, "2020-7":"2023-6"]
with pd.ExcelWriter("按月汇总.xlsx") as writer:
    df_grouped.to_excel(writer, startrow=1)


