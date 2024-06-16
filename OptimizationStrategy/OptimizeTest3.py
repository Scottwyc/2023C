import numpy as np
import pandas as pd
from scipy.optimize import minimize

# Load data
data = pd.read_excel('Q2Info-average.xlsx', index_col=0) # first col as index
print(data)
# row index is 1~6, so i+1 for row index!


def f_i(x, a, b, c):
    # print(a/(x+1e-6) + b * x + c)
    return a/(x+1e-6) + b * x + c

# Objective function (negated for minimization)
# M_i = N_hat_i

num = 2

def objective(vars):
    Pro = 0
    for i in range(6):
        N_hat, P_i = vars[i*num:(i+1)*num]
        R_i, D_i = data.loc[i+1, ['R_i', 'D_i']]
        B_hat = data.loc[i+1, 'b_i_hat']
        Pro += N_hat * ((1 - R_i) * P_i + R_i * (P_i * D_i) ) - B_hat * N_hat
    return -Pro  # Negate for minimizing

# Constraints for SLSQP: list of dictionaries
def constraint_i(i):
    def constraint(vars):
        N_hat, P_i = vars[i*num: (i+1)*num]
        n_i_hat, a_i, b_i, c_i ,l_i, u_i = data.loc[i+1, ['n_i_hat', 'a_i', 'b_i',  'c_i','l_i','u_i']]
        return [N_hat - n_i_hat*(1-0.2), n_i_hat*(1+0.2) - N_hat, 
                N_hat - f_i(P_i, a_i, b_i, c_i)*l_i, f_i(P_i, a_i, b_i, c_i)*u_i - N_hat
                ]
    return constraint

def constraints(vars):
    cons = []
    for i in range(6):
        cons.append({'type': 'ineq', 'fun': constraint_i(i)})
    return cons


# Bounds (None indicates no bound)
# price should not be that high
bounds = [(0, None), (0,None),
          (0,None),   (0, None),
          (0, None), (0,None),
          (0, None), (0,10),
          (0, None), (0,8),
          (0, None), (0,None)] 

# Initial guess
initial_guess = []
for i in range(6):
    N_hat = data.loc[i+1, 'n_i_hat'] 
    P_i = 1
    # B_hat = data.loc[i+1, 'b_i_hat']
    print(N_hat, P_i)
    initial_guess.extend([N_hat, P_i]) 


# Optimization
# result = minimize(objective, initial_guess, method='SLSQP', constraints=constraints(initial_guess), bounds=bounds)
result = minimize(objective, initial_guess, method='SLSQP', constraints=constraints(initial_guess), bounds=bounds)

# print(result)

result_vars = result.x.reshape(6, num)
print("Optimized N_hat, P_i:")
print(result_vars)
print("Maximum Profit:", -result.fun)

print(result.message)
print(result.success)


