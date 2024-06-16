# should fit the data by day, not by month.
# fit N_i_hat and  P_i for days between 23.6.24-23.6.30


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from scipy.optimize import curve_fit
from sklearn.preprocessing import StandardScaler
import numpy as np

file_path ='preprocessed_DATA2.xlsx'
Names = ['YearMonthDay','ItemEncode','singleItemName','category','index_i',	'index_j',
         'sales(kg)',	'price_ij(yuan/kg)','discountLabel']
df = pd.read_excel(file_path, names=Names)
df = df.iloc[:, [0, 4, 6, 7]]
print(df.head(10))

# step 1: aggregate the data by category 


df2 = df.groupby(['YearMonthDay','index_i']).agg({'sales(kg)':'sum'}).reset_index()
print(df2.head(10)) 

df2['weight'] = df['sales(ke)']/ df2['sales(kg)']
# def func1(x, a, b, c):
#     return a/x + b * x + c


# cols = Combine.columns
# print(cols)
# Ps = pd.DataFrame(columns=['Category','a','b','c'])
# A = []
# B = []
# C = []

# Llist = [0.5, 0.4, 0.3, 0.3, 0.4, 0.5]
# Ulist = [1.8, 1.6, 1.8, 1.8, 1.8, 2.0]

# for i in range(6):
#     col1 = cols[i]
#     col2 = cols[i+7] # for weight of a month
#     Combine = Combine.sort_values(by=[col1])
#     Y = Combine[col2].values.reshape(-1, 1)/30  # for each day
#     X = Combine[col1].values.reshape(-1, 1)
#     # scaler = StandardScaler()
#     # X = scaler.fit_transform(X)
#     # Y = scaler.fit_transform(Y)
#     X, Y = X.flatten(), Y.flatten()
    
#     popt, pcov = curve_fit(func1, X, Y)
#     print(popt)
#     # a, b = popt
#     a, b, c = popt
    
#     multi_low = Llist[i]
#     multi_up = Ulist[i]
#     y_pred1 = func1(X,a,b,c)
#     y_pred2 = func1(X,a,b,c)*multi_low
#     y_pred3 = func1(X,a,b,c)*multi_up

#     plt.rcParams['legend.fontsize'] = 8
#     plt.rcParams['legend.loc'] = 'upper right'
#     # plt.rcParams['legend.borderaxespad'] = 0.5
#     # plt.legend(loc='upper right', bbox_to_anchor=(1.05, 1))
    
        
#     plot0 = plt.plot(X,Y, '*', label=f'Original values(K{i+1})')
#     plot1 = plt.plot(X,y_pred1, 'r', label=f'Fit values1')
#     plot2 = plt.plot(X,y_pred2, 'y', label=f'outline_low_{multi_low}')
#     plot3 = plt.plot(X,y_pred3, 'g', label=f'outline_up_{multi_up}')
#     plt.title(f'K{i+1} Sales and Price')
#     plt.legend()
#     # if i == 5:
#     #     plt.savefig(f'fit_all.png')
#     plt.savefig(f'fit_single_{i}_low{multi_low}_up{multi_up}.png')
#     plt.show()
    
    
#     A.append(a)
#     B.append(b)
#     C.append(c)

# Ps['Category'] = ['花叶类','花菜类','水生根茎类','茄类','辣椒类','食用菌']
# Ps['a'] = A
# Ps['b'] = B
# Ps['c'] = C
# print(Ps)

# Ps.to_excel("Fit_a_b_c.xlsx", index=False)
