# get Di from preprocessed_DATA2.xlsx

import pandas as pd
import numpy as np

# Step 1: Load the preprocessed Excel file

Names = ['YearMonthDay','ItemEncode', 'singleItemName','category','index_i', 'index_j', 
'sales(kg)','price_ij(yuan/kg)','discountLabel']
df = pd.read_excel('preprocessed_DATA2.xlsx', names=Names)
# df = pd.read_excel('testOutput.xlsx', names=Names)

df_extract = df
df_extract['discountLabel'] = np.where(df_extract['discountLabel'] == '是','Discount','NoDiscount')

# step 2 : groupby index_i, index_j, discountLabel

# note the level of groupby index!
grouped = df_extract.groupby(['index_i','index_j', 'discountLabel'])


# step 3: get average price for each item for cases of discount and no discount
averagePriceDF  = grouped['price_ij(yuan/kg)'].mean()

# print(averagePriceDF.head(10) )   
print(averagePriceDF)
averagePriceDF.to_excel('averagePriceDF.xlsx')

# step 4 : get d_ij for each item, note no discount case

d_ij_DF = pd.DataFrame( index= averagePriceDF.index )
# then drop the level of discountLabel
d_ij_DF.index = d_ij_DF.index.droplevel('discountLabel')
# drop repeated index of index_j after droplevel!!
d_ij_DF = d_ij_DF.reset_index().drop_duplicates(subset=['index_i','index_j']).set_index(['index_i','index_j'])


d_ij_DF['d_ij'] = 0.0
d_ij_DF['weight'] = 0.0 # float initialization


# print(d_ij_DF.head(10))
print(d_ij_DF)

for i,j,_ in averagePriceDF.index:
    # get discountLabel for i,j and into list
    discountLabels = averagePriceDF.loc[(i,j)].index.get_level_values('discountLabel').tolist()
    if bool('Discount' in discountLabels) & bool('NoDiscount' in discountLabels):
        # Both types of discountLabel exist for i,j
        d_ij_DF.loc[(i,j),'d_ij'] = averagePriceDF.loc[(i,j,'Discount')]/averagePriceDF.loc[ (i,j,'NoDiscount')]
    elif 'NoDiscount' in discountLabels:
        # Only NoDiscount for i,j
        d_ij_DF.loc[(i,j),'d_ij'] = 1
    elif 'Discount' in discountLabels:
        d_ij_DF.loc[(i,j),'d_ij'] = 0.8 # unknown case
        pass

# print(d_ij_DF.head(10))
print(d_ij_DF)


# step 5: get weight coefficent (in its kind) of each item based on the total sales

KindTotalSalesDF = df_extract.groupby(['index_i'])['sales(kg)'].sum()
ItemTotalSalesDF = df_extract.groupby(['index_i','index_j'])['sales(kg)'].sum()

for i,j in ItemTotalSalesDF.index:
    d_ij_DF.loc[(i,j), 'weight'] = ItemTotalSalesDF[i,j]/KindTotalSalesDF[i]

# print(d_ij_DF.head(10)) 
print(d_ij_DF)

# step 6: save d_ij_DF to a new Excel file, with index!! actually index will be saved cols
# d_ij_DF.to_excel('d_ij_weitghtTest.xlsx', index=True)
d_ij_DF.to_excel('d_ij_weitght.xlsx', index = True)

# step 7: load 'd_ij_weitght.xlsx' and get D_i

# index_col=[0,1] for multiindex
# d_ij_weitghtDF = pd.read_excel('d_ij_weitghtTest.xlsx', index_col=[0,1]) 
d_ij_weitghtDF = pd.read_excel('d_ij_weitght_sales.xlsx', index_col=[0,1])

# get D_i  weighted sum for group
# print(d_ij_weitghtDF.head(10))

D_i = pd.DataFrame(index= d_ij_weitghtDF.index)
D_i.index = D_i.index.droplevel('index_j')
D_i = D_i.reset_index().drop_duplicates(subset=['index_i']).set_index(['index_i']) # drop repeated index of index_i

for i,j in d_ij_weitghtDF.index:
    D_i.loc[i, 'D_i'] = np.sum(d_ij_weitghtDF.loc[i]['d_ij'] * d_ij_weitghtDF.loc[i]['weight'])

# print(D_i.head(10))
print(D_i)

# step8: save D_i to a new Excel file
# D_i.to_excel('D_iTest.xlsx')
D_i.to_excel('D_i.xlsx')
