from pysat.examples.rc2 import RC2
from pysat.formula import WCNF

# Define the graph and parameters
V = 5
graph = [
    [0, 25, 30, 0, 0],   # A (index 0)
    [25, 0, 0, 10, 0],   # 1 (index 1)
    [30, 0, 0, 15, 5],   # 2 (index 2)
    [0, 10, 15, 0, 15],  # 3 (index 3)
    [0, 0, 5, 15, 0]     # 4 (index 4)
]
p = 1  # Example limit for the sum of y_j

# Extract unique distances from the graph
unique_distances = set()
for i in range(V):
    for j in range(i + 1, V):
        if graph[i][j] != 0:
            unique_distances.add(graph[i][j])

# Convert set to sorted list
distinct_distances = sorted(list(unique_distances))
print(distinct_distances)

# Define the parameters of the model
M = range(V)  # Example set of indices for y_j
T = range(len(distinct_distances))  # Example set of indices for z_k
N = range(V)  # Example set of indices for i
rho = distinct_distances  # Costs for z_k (radii)

# Calculate the a_ijk matrices
a = []
for k in range(len(distinct_distances)):
    a_k = []
    for i in range(V):
        a_i = []
        for j in range(V):
            if graph[i][j] <= distinct_distances[k] and graph[i][j] != 0:
                a_i.append(1)
            else:
                a_i.append(0)
        a_k.append(a_i)
    a.append(a_k)

for k in range(len(distinct_distances)):
    print(f"a_ijk for rho_{k} = {distinct_distances[k]}:")
    for i in range(V):
        print(a[k][i])
    print()

# Initialize the WCNF formula
wcnf = WCNF()

# Define the variables for PySAT
y_vars = [i + 1 for i in M]
z_vars = [len(y_vars) + i + 1 for i in T]

# Add the constraints to the WCNF
for k in T:
    for i in N:
        clause = [-z_vars[k]] + [a[k][i][j] * y_vars[j] for j in M]
        wcnf.append(clause)

# Add the constraint for center limitation
wcnf.append([y_vars[j] for j in M], weight=p)

# Add the constraint for selection of radii
for k in T:
    wcnf.append([-z_vars[k]], weight=rho[k])

# Solve the Max-SAT problem using RC2
solver = RC2(wcnf)
solution = solver.compute()

if solution:
    print("Solution found:")
    print("Objective value:", solver.cost)
    print("Values for y_j:")
    for j in M:
        print(f"y_{j} = {1 if y_vars[j] in solution else 0}")
    print("Values for z_k:")
    for k in T:
        print(f"z_{k} = {1 if z_vars[k] in solution else 0}")
else:
    print("No solution found")
