from pysat.solvers import Minisat22
from pysat.formula import IDPool, WCNF

# Initialize variable ID pool
vpool = IDPool()

# Example Data
N = [1, 2, 3, 4, 5]  # Demand nodes
M = [1, 2]           # Facility nodes
R = [10, 15, 20, 25, 30, 35, 40, 50, 60, 80]  # Distances
K = range(1, 11)     # Indices for distances
p = 2                # Number of centers

# Variables
z = {k: vpool.id(f'z_{k}') for k in K}  # Radius selection variables
y = {j: vpool.id(f'y_{j}') for j in M}  # Center placement variables

# Initialize weighted CNF formula
wcnf = WCNF()

# Objective function: maximize the sum of radius values
for k in K:
    wcnf.append([z[k]], weight=R[k-1])

# Example adjacency matrix for distances
# d[i][j] represents the distance between demand node i and facility node j
d = [
    [25, 90],
    [35, 45],
    [50, 55],
    [70, 30],
    [90, 60]
]

# Constraint: Coverage
for i in range(len(N)):
    for k in K:
        clause = [-z[k]]  # z_k = 0 if not selected
        for j in range(len(M)):
            if d[i][j] <= R[k-1]:
                clause.append(y[j+1])  # Add y_j if distance constraint is satisfied
        wcnf.append(clause)

# Constraint: Limit the number of centers
wcnf.append([y[j] for j in M], weight=p)

# Constraint: Select exactly one radius
wcnf.append([z[k] for k in K], weight=1)

# Convert WCNF object to a list of clauses
clauses = wcnf.hard + [[lit] for lit in wcnf.soft]

# Solve the problem
solver = Minisat22(bootstrap_with=clauses)
if solver.solve():
    model = solver.get_model()
    print("Satisfiable Model: ", model)
else:
    print("Unsatisfiable")
