# Q1.1

I need to base on the example shown in the md file, and use the data in TestData.xlsx, to generate python code to build and solve the optimization problem. Note that TestData.xlsx is given in the md

# A1.1

a simplified example using:
from scipy.optimize import linprog

# Q1.2

how can I get the value of P_i and M_i from the result of linprog, and output them as a table?

# A1.2

```python
# Assuming P_i and M_i are the first two elements of the solution vector
P_i = result.x[0]
M_i = result.x[1]

# Step 4: Create and output a table
# Using pandas for a nicer table format
df = pd.DataFrame({'P_i': [P_i], 'M_i': [M_i]})
print(df)
```
# Q2.1

Based on "the example" shown in the md file, use the data in TestData.xlsx(given in the md), to generate python code to build and solve the optimization problem. Note that do not need to use linprog.

# A2.2
give a detailed snippet


# Q2.3

I mean, 'N_i' is the uncertain variable with its own constraints([0, n_i], and n_i is given in the TestData.xlsx), which is not given in the TestData.xlsx. Please make changes in "Bounds"

# A2.3
```python
# Bounds
# Adjust bounds for 'M' based on 'N_i's constraints ([0, n_i])
bounds = [(0, data['n_i'][i]) for i in range(6)] + [(None, None)]*6  # 'P' is unbounded

```

# Q2.4
But then you lose the variables 'N_i' in the problem, and I suggest that you can add 'N_i' into variables to solve, with constraints given in the md.


# A2.4
```python
# Bounds
# Bounds for N_i based on [0, n_i], M and P as previously defined
bounds = [(0, data['n_i'][i]) for i in range(6)] + [(0, None)]*6 + [(None, None)]*6

```

# Q2.5
still, the bounds do not show the constraints "M_i >= N_i"

# A2.5
```python
# Constraint M_i >= N_i
def constraint_mi_ni(vars):
    N, M = vars[:6], vars[6:12]
    return M - N  # This should be non-negative

# Collecting all constraints
constraints = ({'type': 'ineq', 'fun': constraint_mi_ni})

# Bounds
# Bounds for N_i based on [0, n_i], for M and P as previously defined
bounds = [(0, data['n_i'][i]) for i in range(6)] + [(0, None)]*6 + [(None, None)]*6

# Solve
result = minimize(objective, initial_guess, method='SLSQP', bounds=bounds, constraints=constraints)

```

# Q3.1

I need you to help me with python code based on soveQ2.md to solve Q2. I need preprocess first.

# Q3.2

if the key vaule of the dict_total is a list, how can I map into different cols










