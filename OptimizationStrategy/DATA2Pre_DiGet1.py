# preprocess DATA2.xlsx for getting D_i

import pandas as pd
import json

# Step 1: Load the Excel file
df = pd.read_excel('../ProblemC/DATA2.xlsx')
# df = pd.read_excel('testDATA2.xlsx')

# Step 2: Drop rows where 销售类型 is 退货
df = df[df['销售类型'] != '退货']

# Step 3: Filter for dates: 2023.6.24-6.30
df['销售日期'] = pd.to_datetime(df['销售日期'])  # into datetime
df = df[
        (df['销售日期'].dt.year == 2023 )
    &  (df['销售日期'].dt.month == 6 )
    & df['销售日期'].dt.day.between(24, 30, inclusive='both') 
        ]

print(df.head(10) )

# step 4: use dict_total to build category col
with open("dict_total.json", "r") as file:
    dict_total = json.load(file)  # {"单品编码":["单品名称", "分类名称", [i,j]]}

# print(dict_total.keys() )
# print( type(list(dict_total.keys())[0])  )
print(df['单品编码'].head(10) )

# list of col index for list of keyvalues and set Series for each col
df[ ['singleItemName', 'category', 'index_i','index_j'] ] = df['单品编码'].apply(
    lambda x: pd.Series(dict_total.get(str(x), [None, None, None,None]))
) # should transform into str for key!


df['YearMonthDay'] = df['销售日期'].dt.strftime('%Y-%m-%d')

df['ItemEncode'] = df['单品编码']


# Step 5: Select required columns
df = df[['YearMonthDay' ,'ItemEncode', 'singleItemName', 'category', 'index_i','index_j', '销量(千克)', '销售单价(元/千克)', '是否打折销售']]

# The DataFrame 'df' is now preprocessed and ready for further analysis.

# Step 6: Save the preprocessed DataFrame to a new Excel file
df.to_excel('preprocessed_DATA2.xlsx', index=False)
# df.to_excel('testOutput.xlsx', index=False)






