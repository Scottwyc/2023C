from scipy.optimize import minimize
import numpy as np
import pandas as pd

# Step 2: Load Data
data = pd.read_excel('TestData.xlsx')
n = np.array(data['n_i'])
b = np.array(data['b_i'])
D = np.array(data['D_i'])
R = np.array(data['R_i'])
L = np.array(data['L_i'])
U = np.array(data['U_i'])

# For demonstration, let's assume some values for n, b, D, R, L, and U
# n = np.array([100, 150, 200, 90, 30, 100])
# b = np.array([2.4, 1.5, 4.9, 3, 4.3, 1])
# D = np.array([0.9, 0.5, 0.4, 0.6, 0.8, 0.7])
# R = np.array([0.2, 0.3, 0.4, 0.5, 0.6, 0.7])
# L = np.array([1.1, 1.2, 1.3, 1.4, 1.5, 1.6])
# U = np.array([2.2, 2.1, 3.2, 3.5, 4.5, 1.7])

# Step 3: Setup Objective Function
def objective(vars):
    M, P, N = vars[:6], vars[6:12], vars[12:]
    Pro = -np.sum(N * ((1 - R) * P + R * (P * D) - b * M))
    return Pro

def f_i( N, i):
    return 10.0*i/N + 0.1*i*N + 100

# Step 4: Define Constraints and Bounds
constraints = []
for i in range(6):
    constraints.append({'type': 'ineq', 'fun': lambda vars, i=i: vars[i] - vars[12+i]})  # M_i >= N_i
    constraints.append({'type': 'ineq', 'fun': lambda vars, i=i: n[i] - vars[i]})  # M_i <= n_i
    constraints.append({'type': 'ineq', 'fun': lambda vars, i=i: vars[6+i] - ( f_i(vars[12+i], i)+L[i] ) })  # P_i >= L(N)
    constraints.append({'type': 'ineq', 'fun': lambda vars, i=i: ( f_i(vars[12+i], i)+U[i] ) - vars[6+i]})  # P_i <= U(N)
    constraints.append({'type': 'ineq', 'fun': lambda vars, i=i: n[i] - vars[12+i]})  # N_i <= n_i

bounds = [(0, ni) for ni in n] + [(0, None)] * 6 + [(0, ni) for ni in n]  # Bounds for M, P, and N

# Step 5: Solve the Problem
initial_guess = np.concatenate([n / 2, (L + U) / 2, n / 2])
result = minimize(objective, initial_guess, method='SLSQP', bounds=bounds, constraints=constraints)

if result.success:
    optimized_M, optimized_P, optimized_N = result.x[:6], result.x[6:12], result.x[12:]
    print("Optimized M:", optimized_M)
    print("Optimized P:", optimized_P)
    print("Optimized N:", optimized_N)
    print("Maximum Profit:", -result.fun)
else:
    print("Optimization failed:", result.message)