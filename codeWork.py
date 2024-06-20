from pysat.formula import CNF
from pysat.pb import PBEnc, EncType as pbenc
from pysat.card import CardEnc, EncType as cardenc
from pysat.solvers import Solver

# Example graph data
V = 5
graph = [
    [0, 25, 30, 0, 0],   # A (index 0)
    [25, 0, 0, 10, 0],   # 1 (index 1)
    [30, 0, 0, 15, 5],   # 2 (index 2)
    [0, 10, 15, 0, 15],  # 3 (index 3)
    [0, 0, 5, 15, 0]     # 4 (index 4)
]
unique_distances = set()
for i in range(len(graph)):
    for j in range(len(graph[i])):
        if graph[i][j] != 0:
            unique_distances.add(graph[i][j])
distinct_distances = sorted(list(unique_distances))
print("Distinct distances (rho values):", distinct_distances)

# Set of radii
T = list(range(1, len(distinct_distances) + 1))
# # Set of radii
# T = list(range(1, 6))  # Radii values from 1 to 5

# Example radius weights
radii_weights = list(range(1, len(distinct_distances) + 1))

# Number of centers
p = 1  # Example: selecting exactly 1 center

cnf = CNF()

# Soft constraint: maximize sum of radii weights for selected centers
# soft_clause = PBEnc.equals(lits=T, weights=radii_weights, bound=p, encoding=pbenc.sortnetwrk)
# cnf.extend(soft_clause.clauses)

# Ensure each vertex is covered by at least one center within the selected radius:
for i in range(V):
    for k in T:
        clause = []
        for j in range(V):
            if graph[i][j] > 0:
                clause.append(j + 1)  # Literal y_j (center j covers vertex i)
        clause.append(-(k + 1))  # Literal -z_k (radius k not selected)
        cnf.append(clause)

# Limit the number of selected centers to p:
atmost_clause = CardEnc.atmost(list(range(1, V + 1)), bound=p, encoding=cardenc.sortnetwrk)
cnf.extend(atmost_clause.clauses)

# # Select exactly one radius among the set T:
equals_clause = CardEnc.equals(T, bound=1, encoding=cardenc.sortnetwrk)
cnf.extend(equals_clause.clauses)




with Solver() as solver:
    solver.append_formula(cnf)
    sat = solver.solve()

    if sat:
        model = solver.get_model()
        print("Satisfiable. Model:", model)
        
        # Extracting z_k values
        z = {k: 1 if (k + 6) in model else 0 for k in T}
        print("z_k values:", z)
        
        # Extracting y_j values
        y = {j: 1 if (j + 1) in model else 0 for j in range(V)}
        print("y_j values:", y)
        
        # Extracting a_ijk values
        a = {}
        for i in range(V):
            for j in range(V):
                for k in T:
                    if graph[i][j] > 0:
                        a[(i, j, k)] = 1 if ((j + 1) in model and -(k + 6) not in model) else 0
        print("a_ijk values:")
        for key, value in a.items():
            print(f"a_{key} = {value}")
        
        # Extracting rho values
        rho = {k: radii_weights[k-1] for k in T if z[k] == 1}
        print("rho values:", rho)
    else:
        print("Unsatisfiable.")
