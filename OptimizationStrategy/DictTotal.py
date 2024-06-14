# build dict_total based on goods_ij.xlsx

import numpy as np
import pandas as pd
import json

# dtype can be a dict to designate the type of each col!
# use np.int64 for the encoding of keyCol!! 102900005117056 is long
df = pd.read_excel("../Preprocess/goods_ij.xlsx", dtype= {0:np.int64, 1:str, 2:int, 3:str, 4:int, 5:int})

# type of keyCol should be int64: like 102900005117056
# but in dict_total, the key still transfered to str??
keyCol = df.iloc[:, 0]
# print( type(keyCol[0]))

singleNameCol = df.iloc[:,1]
# print( type(singleNameCol[0]))

categoryCol = df.iloc[:, 3]
icol = df.iloc[:, 4]
jcol = df.iloc[:, 5]

# zip the (i,j)
# indexPairCol = list(zip(icol, jcol))
# print(icol)
# print(indexPairCol)

# then build dict_total

dict_total = {}

for key, singleName, category, i, j in zip(keyCol, singleNameCol,categoryCol, icol,jcol):
    dict_total[key] = [singleName, category, i,j]

# print(dict_total) 
print(dict_total.keys())
print( type(list(dict_total.keys())[0]) )


print(dict_total.get(102900005117056, [None, None, None]) )


# save dict_total into json
with open('dict_total.json', 'w') as file:
    json.dump(dict_total, file)



