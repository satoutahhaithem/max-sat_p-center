from pysat.formula import WCNF
from pysat.pb import PBEnc, EncType
from pysat.card import CardEnc
from pysat.examples.rc2 import RC2

nbrNodes = 5
graph = [
    [0, 25, 30, 0, 0],   # A (index 0)
    [25, 0, 0, 10, 0],   # 1 (index 1)
    [30, 0, 0, 15, 5],   # 2 (index 2)
    [0, 10, 15, 0, 15],  # 3 (index 3)
    [0, 0, 5, 15, 0]     # 4 (index 4)
]
p = 1   # Example limit for the sum of y_j

# Extract unique distances from the graph
unique_distances = set()
for i in range(nbrNodes):
    for j in range(i + 1, nbrNodes):
        if graph[i][j] != 0:
            unique_distances.add(graph[i][j])

# Convert set to sorted list
distinct_distances = sorted(list(unique_distances))

# Define parameters
all_Nodes = range(1, nbrNodes + 1)  # Indices for y_j (vertices)
index_z_k = range(1, len(distinct_distances) + 1)  # Indices for z_k (radii)
demandNodes = range(1, nbrNodes - p + 1)  # Indices for i (vertices excluding the last p)
rho = distinct_distances  # Costs for z_k (radii)

constraints = WCNF()

# Define z and y variables
z_vars = [k for k in index_z_k]
y_vars = [k + len(index_z_k) for k in all_Nodes]

# Print variable mappings for debugging
print("Variable mappings:")
print("z_vars:", z_vars)
print("y_vars:", y_vars)

# Soft constraint
for k in index_z_k:
    weight = rho[k - 1]  # Weight calculation
    clause = [-z_vars[k - 1]]  # Negative index for soft clause
    constraints.append(clause, weight)

# Function to calculate var_a_ijk
def var_a_ijk(i, j, k, nbrNodes, len_distinct_distances):
    return (i - 1) * nbrNodes * len_distinct_distances + (j - 1) * len_distinct_distances + k

# Calculate a_ijk and add constraints
for k in index_z_k:
    for i in demandNodes:
        a_i = []
        for j in all_Nodes:
            if graph[i - 1][j - 1] <= distinct_distances[k - 1] and graph[i - 1][j - 1] != 0:
                a_i.append(var_a_ijk(i, j, k, nbrNodes, len(distinct_distances)))  # Positive literal
        if a_i:
            geqCons = PBEnc.geq(lits=a_i, weights=[1] * len(a_i), bound=1, encoding=EncType.sortnetwrk)
            constraints.extend(geqCons)

# At most p y_j variables are true
amo_clause = CardEnc.atmost(lits=y_vars, bound=p, encoding=EncType.sortnetwrk)
constraints.extend(amo_clause)

# Exactly 1 z_k variable is true
equa_clause = CardEnc.equals(lits=z_vars, bound=1, encoding=EncType.sortnetwrk)
constraints.extend(equa_clause)

# Print the constraints for debugging
print("Constraints (WCNF):")
for clause in constraints.hard:
    print(clause)
print("Soft constraints:")
for weight, clause in zip(constraints.wght, constraints.soft):
    print(weight, clause)

# Solve the problem using RC2
with RC2(constraints, solver="cadical153") as solver:
    for model in solver.enumerate():
        print('Model has cost:', solver.cost)
        print('Model:', model)
        print("Values for y_j:")
        for j in all_Nodes:
            print(f"y_{j} = {1 if model[y_vars[j - 1] - 1] > 0 else 0}")
        print("Values for z_k:")
        for k in index_z_k:
            print(f"z_{k} = {1 if model[z_vars[k - 1] - 1] > 0 else 0}")
        break
