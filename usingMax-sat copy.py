from pysat.formula import WCNF
from pysat.pb import PBEnc, EncType
from pysat.card import CardEnc
from pysat.examples.rc2 import RC2
import heapq

def dijkstra(vertices, graph, sources):
    dist = [[float('inf')] * vertices for _ in range(len(sources))]
    pq = []
    for i, src in enumerate(sources):
        dist[i][src] = 0
        heapq.heappush(pq, (0, src, i))
    while pq:
        current_dist, u, src_index = heapq.heappop(pq)
        if current_dist > dist[src_index][u]:
            continue
        for v in range(vertices):
            if graph[u][v] > 0:
                new_dist = dist[src_index][u] + graph[u][v]
                if new_dist < dist[src_index][v]:
                    dist[src_index][v] = new_dist
                    heapq.heappush(pq, (new_dist, v, src_index))
    return dist

# Problem parameters
nbrNodes = 3
g = [
    [0, 25, 15],  
    [25, 0, 5],   
    [15, 5, 0],       
]
p = 1  # Set p to 1

# Compute shortest paths using Dijkstra
sources = list(range(nbrNodes))
graph = dijkstra(nbrNodes, g, sources)
for row in graph:
    print(row)
print("###########################################################################")

# Extract unique distances
unique_distances = set()
for i in range(len(graph)):
    for j in range(len(graph[i])):
        if graph[i][j] != 0:
            unique_distances.add(graph[i][j])
distinct_distances = sorted(list(unique_distances))

# Define variables
all_Nodes = range(nbrNodes)
index_z_k = range(len(distinct_distances))
rho = distinct_distances

constraints = WCNF()
top_id = 0

# Variable mappings
y_vars = [j + 1 for j in all_Nodes]
z_vars = [k + nbrNodes + 1 for k in index_z_k]
top_id = max(z_vars)

print("Variable mappings:")
print("z_vars:", z_vars)
print("y_vars:", y_vars)

# Adding soft constraints
for k in index_z_k:
    weight = rho[k]
    clause = [-z_vars[k]]
    constraints.append(clause, weight)

globalEncType = EncType.sortnetwrk

# Adding hard constraints for the distance matrix
for i in all_Nodes:
    for k in index_z_k:
        var_y = []
        for j in all_Nodes:
            if graph[i][j] <= distinct_distances[k]:
                var_y.append(y_vars[j])
        if var_y:
            geq_clause = PBEnc.geq(lits=var_y + [-z_vars[k]], bound=1, encoding=globalEncType, top_id=top_id)
            constraints.extend(geq_clause)
            top_id = max(top_id, geq_clause.nv)

# Adding constraint: Sum of y_j <= p
amo_clause = CardEnc.atmost(lits=y_vars, bound=p, encoding=globalEncType, top_id=top_id)
constraints.extend(amo_clause)
top_id = max(top_id, amo_clause.nv)

# Adding constraint: Sum of z_k == 1
equa_clause = CardEnc.equals(lits=z_vars, bound=1, encoding=globalEncType, top_id=top_id)
constraints.extend(equa_clause)
top_id = max(top_id, equa_clause.nv)

print("Constraints (WCNF):")
for clause in constraints.hard:
    print(clause)
print("Soft constraints:")
for weight, clause in zip(constraints.wght, constraints.soft):
    print(weight, clause)

with RC2(constraints, solver="cadical153") as solver:
    for model in solver.enumerate():
        print('Model has cost:', solver.cost)
        print('Model:', model)
        print("Values for y_j:")
        for j in all_Nodes:
            print(f"y_{j+1} = {1 if model[y_vars[j] - 1] > 0 else 0}")
        print("Values for z_k:")
        for k in index_z_k:
            print(f"z_{k+1} = {1 if model[z_vars[k] - 1] > 0 else 0}")
        break
