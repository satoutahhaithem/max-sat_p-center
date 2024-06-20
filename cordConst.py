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
p = 1  # Example: selecting exactly 2 centers

cnf = CNF()

# Soft constraint: maximize sum of radii weights for selected centers
soft_clause = PBEnc.equals(lits=T, weights=radii_weights, bound=p, encoding=pbenc.sortnetwrk)
cnf.extend(soft_clause.clauses)

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

# Select exactly one radius among the set T:
equals_clause = CardEnc.equals(T, bound=1, encoding=cardenc.sortnetwrk)
cnf.extend(equals_clause.clauses)

with Solver() as solver:
    solver.append_formula(cnf)
    sat = solver.solve()

    if sat:
        model = solver.get_model()
        print("Satisfiable. Model:", model)
    else:
        print("Unsatisfiable.")
