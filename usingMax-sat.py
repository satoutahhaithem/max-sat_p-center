from pysat.formula import *
from pysat.pb import EncType as pbenc
from pysat.pb import *
from pysat.card import *
from pysat.solvers import *
from pysat.examples.rc2 import RC2
from pysat.formula import WCNF
import sys

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
all_Nodes = range(nbrNodes)  # Indices for y_j (vertices)
index_z_k = range(len(distinct_distances))  # Indices for z_k (radii)
demandNodes = range(nbrNodes - p)  # Indices for i (vertices excluding the last p)
rho = distinct_distances  # Costs for z_k (radii)




constraints = WCNF()

z=range(len(index_z_k))
y=range(nbrNodes)
print (z)
# Soft constraint 
for k in index_z_k:
    weight = rho[k] # Example weight calculation
    clause = [-z[k]]  # Negative index for soft clause
    constraints.append(clause, weight)
###################################calculate a_ijk #########################################
def var_a_ijk(i, j, k ):
    return (i-1)*nbrNodes *len(distinct_distances)  + (j-1)*nbrNodes + k



for k in range(len(distinct_distances)):
    for i in range(nbrNodes):
        a_i = []
        yWeight=[]
        for j in range(nbrNodes):
            if graph[i][j] <= distinct_distances[k] and graph[i][j] != 0:
                a_i.append(var_a_ijk(i, j, k))  # Positive literal
                yWeight.append(y[j])
            else:
                a_i.append(-var_a_ijk(i, j, k))  # Negative literal
                yWeight.append(y[j])
        geqCons = PBEnc.geq(lits=a_i, weights=yWeight, bound=k, encoding=pbenc.sortnetwrk)
        constraints.extend(geqCons)
#####################################################################################

for j in all_Nodes :
    amo_clause = CardEnc.atmost(lits=y, bound=p,encoding=EncType.cardnetwrk)


for k in index_z_k :
    equa_clause = CardEnc.atmost(lits=z, bound=1,encoding=EncType.cardnetwrk)

with RC2(constraints, solver="Cadical153") as solver:
    for model in solver.enumerate():
        print('Model has cost:', solver.cost)
        # print('Model:', solver.model)

#         display_assignments_by_slot_with_counts(model, slots, papers_range, conference_sessions)
#         break  


# # Hard constraint 
# for k in index_z_k: 
#     for i in demandNodes : 
#         for j in facility_Nodes : 
            






# # Soft clauses for the objective (minimizing the sum of radii)
# for k in T:
#     clause = [-rho[k], k + 1]  # Negate rho[k] and use 1-indexed variable
#     wcnf.append(clause)

# # Hard clauses for vertex coverage constraint
# for i in range(V):
#     for k in T:
#         clause = []
#         for j in M:
#             if a[k][i][j] == 1:
#                 clause.append(1 + j)  # Convert 0-indexed j to 1-indexed
#         if clause:
#             clause.append(len(M) + 1 + k)  # z_k variable
#             wcnf.append(clause)

# # Hard clause for center limitation constraint
# clause = [1 + j for j in M]
# wcnf.append(clause)

# # Use PBEnc to handle pseudo-Boolean constraints
# pb_enc = PBEnc()

# z_vars = [pb_enc.new_var() for _ in T]
# at_most_p = PBEnc(polarity=True, encoding=PBEnc.PB_SW)
# wcnf.extend(pb_enc.atmost(z_vars, p, condition=z_vars, encoding=at_most_p))

# # Create a solver instance
# solver = Solver(name='g4')

# # Solve the Max-SAT problem
# solver.append_formula(wcnf.clauses)
# if solver.solve():
#     model = solver.get_model()
#     print("Solution found:")
#     print("Objective value:", sum(rho[k] for k in T if model[k]))
#     print("Values for y_j:")
#     for j in M:
#         print(f"y_{j} = {1 if model[j] > 0 else 0}")
#     print("Values for z_k:")
#     for k in T:
#         print(f"z_{k} = {1 if model[len(M) + k] > 0 else 0}")
# else:
#     print("No solution found")
