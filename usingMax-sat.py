from pysat.formula import WCNF
from pysat.pb import PBEnc, EncType
from pysat.card import CardEnc
from pysat.examples.rc2 import RC2
import heapq
def dijkstra(vertices, graph, sources):
    # Initialize distances with infinity for all vertices
    dist = [[float('inf')] * vertices for _ in range(len(sources))]
    
    # Priority queue to store vertices and their distances
    pq = []

    # Initialize distances for each source vertex
    for i, src in enumerate(sources):
        dist[i][src] = 0
        heapq.heappush(pq, (0, src, i))  # (distance, vertex, source_index)

    while pq:
        current_dist, u, src_index = heapq.heappop(pq)

        # If current distance is greater than the recorded distance, skip
        if current_dist > dist[src_index][u]:
            continue

        # Traverse neighbors of u
        for v in range(vertices):
            if graph[u][v] > 0:  # Only consider non-zero edges
                new_dist = dist[src_index][u] + graph[u][v]

                # If found shorter path to v, update distance and push to priority queue
                if new_dist < dist[src_index][v]:
                    dist[src_index][v] = new_dist
                    heapq.heappush(pq, (new_dist, v, src_index))

    return dist
nbrNodes = 3
g = [
    [0, 25, 0],  
    [10, 0, 20],   
    [15, 5, 0],       
]
# nbrNodes = 5
# g = [
#     [0, 16, 31, 0, 0],   # A (index 0)
#     [23, 0, 0, 10, 0],   # 1 (index 1)
#     [30, 0, 0, 14, 5],   # 2 (index 2)
#     [0, 10, 15, 0, 13],  # 3 (index 3)
#     [0, 0, 4, 21, 0]     # 4 (index 4)
# ]
p=2
sources = list(range(nbrNodes)) 
graph = dijkstra(nbrNodes, g, sources)
for row in graph:
    print (row)
print("###########################################################################")

# Extract unique distances from the graph
unique_distances = set()

# Iterate through the matrix
for i in range(len(graph)):
    for j in range(len(graph[i])):
        if graph[i][j] != 0:
            unique_distances.add(graph[i][j])

# Convert the set to a sorted list
distinct_distances = sorted(list(unique_distances))

# Define parameters
all_Nodes = range(1, nbrNodes + 1)  # Indices for y_j (vertices)
index_z_k = range(1, len(distinct_distances) + 1)  # Indices for z_k (radii)
demandNodes = range(1, nbrNodes )  # Indices for i (vertices excluding the last p)
rho = distinct_distances  # Costs for z_k (radii)
print("the distinct distanc is ",distinct_distances)
constraints = WCNF()

# Define z and y variables
y_vars = [j for j in all_Nodes]
z_vars = [k + nbrNodes for k in index_z_k]

# Print variable mappings for debugging
print("Variable mappings:")
print("z_vars:", z_vars)
print("y_vars:", y_vars)

# Soft constraint
for k in index_z_k:
    weight = rho[k - 1]  # Weight calculation
    clause = [-z_vars[k - 1]]  # Negative index for soft clause
    constraints.append(clause, weight)
globalEncType = EncType.sortnetwrk
# Function to calculate var_a_ijk
# def var_a_ijk(i, j, k, nbrNodes, len_distinct_distances):
#     return (i - 1) * nbrNodes * len_distinct_distances + (j - 1) * len_distinct_distances + k

# # Calculate a_ijk and add constraints
# for k in index_z_k:
#     for i in all_Nodes:
        
#         for j in all_Nodes:
#             a_i = []
#             wei
#             if graph[i - 1][j - 1] <= distinct_distances[k - 1] and graph[i - 1][j - 1] != 0:
#                 a_i.append(var_a_ijk(i, j, k, nbrNodes, len(distinct_distances)))  # Positive literal
#         if a_i:
#             geqCons = PBEnc.geq(lits=y_vars, weights=a_i, bound=1, encoding=EncType.sortnetwrk)
#             constraints.extend(geqCons)
for i in all_Nodes:
    for k in index_z_k :
         var_y=[]
         for j in all_Nodes:
            if graph[i-1][j-1] <= distinct_distances[k-1] and graph[i-1][j-1] != 0:
                var_y.append(y_vars[j-1])
         print(y_vars)
         print (z_vars[k - 1])
         if var_y:
            geq_clause = PBEnc.atleast(lits=var_y + [-z_vars[k - 1]], bound=1, encoding=globalEncType)
            constraints.extend(geq_clause)

# At most p y_j variables are true
amo_clause = CardEnc.atmost(lits=y_vars, bound=p, encoding=globalEncType)
constraints.extend(amo_clause)

# Exactly 1 z_k variable is true
equa_clause = CardEnc.equals(lits=z_vars, bound=1, encoding=globalEncType)
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
