import numpy as np
import pandas as pd
from scipy.optimize import minimize

# Load data
data = pd.read_excel('Q2Info-average.xlsx', index_col=0) # first col as index
print(data)
# row index is 1~6, so i+1 for row index!

# Define the function f_i(P_i)
# def f_i(P_i, a_i, b_i):
#     # set max P_i threshold
#     if P_i > 25:
#         return 0
#     print("fitted N_hat:",end="  ")
#     print(np.exp(a_i * P_i + b_i) / (1 + np.exp(a_i * P_i + b_i)))
#     return np.maximum(np.exp(a_i * P_i + b_i) / (1 + np.exp(a_i * P_i + b_i)), 0)

def f_i(x, a, b, c):
    return a/x + b * x + c

# Objective function (negated for minimization)
def objective(vars):
    Pro = 0
    for i in range(6):
        N_hat, P_i, M_i, B_hat = vars[i*4:(i+1)*4]
        R_i, D_i = data.loc[i+1, ['R_i', 'D_i']]
        Pro += N_hat * ((1 - R_i) * P_i + R_i * (P_i * D_i) - B_hat * M_i)
    return -Pro  # Negate for minimizing

# Constraints
def constraints(vars):
    cons = []
    for i in range(6):
        N_hat, P_i, M_i, B_hat = vars[i*4:(i+1)*4]
        # row index is 1~6, so i+1 ?
        # n_i_minus, n_i_plus, b_i_minus, b_i_plus, a_i, b_i = data.loc[i+1, ['n_i_minus', 'n_i_plus', 'b_i_minus', 'b_i_plus', 'a_i', 'b_i']]
        n_i_hat, b_i_hat, a_i, b_i, c_i ,l_i, u_i = data.loc[i+1, ['n_i_hat', 'b_i_hat', 'a_i', 'b_i',  'c_i','l_i','u_i']]

        # alwasys /ge as 'ineq' in scipy
        # N_hat bounds
        cons.append({'type': 'ineq', 'fun': lambda vars: vars[i*4] - n_i_hat*0.95}) 
        cons.append({'type': 'ineq', 'fun': lambda vars: n_i_hat*1.05 - vars[i*4]})
        
        # B_hat bounds
        cons.append({'type': 'ineq', 'fun': lambda vars: vars[i*4+3] - b_i_hat*0.95})
        cons.append({'type': 'ineq', 'fun': lambda vars: b_i_hat*1.05 - vars[i*4+3]})
        cons.append({'type': 'ineq', 'fun': lambda vars: vars[i*4+3] })

        # M_i bounds
        # cons.append({'type': 'ineq', 'fun': lambda vars: vars[i*4+2] - vars[i*4]})
        # cons.append({'type': 'ineq', 'fun': lambda vars: n_i_hat*1.2  - vars[i*4+2]})
        cons.append({'type': 'eq', 'fun': lambda vars: vars[i*4+2] - vars[i*4]})
        
        # # N_hat in [f_i(P_i)*0.95, f_i(P_i)*1.05]
        cons.append({'type': 'ineq', 'fun': lambda vars: vars[i*4] - f_i(vars[i*4+1], a_i, b_i, c_i)*l_i } ) 
        cons.append({'type': 'ineq', 'fun': lambda vars: f_i(vars[i*4+1], a_i, b_i, c_i)*u_i - vars[i*4]})
        
        # P_i >= 0 & P_i <= 20
        cons.append({'type': 'ineq', 'fun': lambda vars: vars[i*4+1]})
        cons.append({'type': 'ineq', 'fun': lambda vars: 20 - vars[i*4+1]})
        
    return cons

# Initial guess
initial_guess = []
for i in range(6):
    N_hat = data.loc[i+1, 'n_i_hat'] 
    P_i = 10
    M_i = N_hat
    B_hat = data.loc[i+1, 'b_i_hat']
    print(N_hat, P_i, M_i, B_hat)
    initial_guess.extend([N_hat, P_i, M_i, B_hat]) 


# Bounds (None indicates no bound)
bounds = [(0, None)] * 24

# Optimization
result = minimize(objective, initial_guess, method='trust-constr', constraints=constraints(initial_guess), bounds=bounds)

# print(result)

if result.success:
    result_vars = result.x.reshape(6, 4)
    print("Optimized N_hat, P_i, M_i, B_hat:")
    print(result_vars)
    print("Maximum Profit:", -result.fun)
else:
    print("Optimization failed:", result.message)
    result_vars = result.x.reshape(6, 4)
    print("Optimized N_hat, P_i, M_i, B_hat:")
    print(result_vars)
    print("Maximum Profit:", -result.fun)

