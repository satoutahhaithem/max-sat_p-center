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

# Set of radii
T = list(range(1, 6))  # Radii values from 1 to 5

# Example radius weights
radii_weights = [1, 2, 3, 4, 5]

# Number of centers
p = 1  # Example: selecting exactly 1 center

cnf = CNF()

# Soft constraint: maximize sum of radii weights for selected centers
weights_dict = {k: radii_weights[k - 1] for k in T}  # {1: 1, 2: 2, ..., 5: 5}
soft_clause = PBEnc.atleast(lits=T, weights=weights_dict, bound=p, encoding=pbenc.sortnetwrk)
cnf.extend(soft_clause.clauses)
print("Soft clause:", soft_clause.clauses)

# Ensure each vertex is covered by at least one center within the selected radius:
for i in range(V):
    for k in T:
        clause = []
        for j in range(V):
            if graph[i][j] > 0:
                clause.append((j + 1) + (V * k))  # Literal y_j (center j covers vertex i within radius k)
        clause.append(-(V * k + i + 1))  # Literal -z_k (radius k not selected)
        cnf.append(clause)

# Limit the number of selected centers to p:
atmost_clause = CardEnc.atmost(list(range(1, V + 1)), bound=p, encoding=cardenc.sortnetwrk)
cnf.extend(atmost_clause.clauses)
print("Center limitation clause:", atmost_clause.clauses)

# Select exactly one radius among the set T:
equals_clause = CardEnc.equals(T, bound=1, encoding=cardenc.sortnetwrk)
cnf.extend(equals_clause.clauses)
print("Selection of radii clause:", equals_clause.clauses)

# Create a solver instance
solver = Solver()

# Add the clauses to the solver
solver.append_formula(cnf)

# Solve the problem
sat = solver.solve()

if sat:
    model = solver.get_model()
    print("Satisfiable. Model:", model)
else:
    print("Unsatisfiable.")
    # Print soft clause for debugging
    print("Soft clause:", soft_clause.clauses)

    # Print first few vertex coverage clauses for debugging
    for clause in cnf.clauses[-V * len(T): -V * len(T) + 10]:  # Adjust indices as needed
        print("Vertex coverage clause:", clause)

    # Print center limitation clauses for debugging
    print("Center limitation clause:", atmost_clause.clauses)

    # Print selection of radii clauses for debugging
    print("Selection of radii clause:", equals_clause.clauses)
    print("Unsatisfiable.")