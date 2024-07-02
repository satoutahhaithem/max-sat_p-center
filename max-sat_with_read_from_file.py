from pysat.formula import WCNF
from pysat.pb import PBEnc, EncType
from pysat.card import CardEnc
from pysat.examples.rc2 import RC2
import heapq

def create_adjacency_matrix(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        
    # Read the size of the matrix and ignore the 'p' parameter
    size_info = list(map(int, lines[0].strip().split()))
    n = size_info[0]  # number of nodes
    e = size_info[1]  # number of edges
    p = size_info[2]  # additional parameter
    
    # Initialize adjacency matrix with zeros
    adj_matrix = [[0] * n for _ in range(n)]
    
    # Read the edges and weights
    for line in lines[1:]:
        i, j, weight = map(int, line.strip().split())
        # For undirected graph, set both adj_matrix[i-1][j-1] and adj_matrix[j-1][i-1] to weight
        adj_matrix[i-1][j-1] = weight
        adj_matrix[j-1][i-1] = weight
    
    return adj_matrix, n, e, p

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


# Specify the filename
filename = 'instances/pmed1.txt'

# Create the adjacency matrix and get additional parameters
adj_matrix, n, e, p = create_adjacency_matrix(filename)

# Print the additional parameters
print(f"Number of nodes: {n}")
print(f"Number of edges: {e}")
print(f"Additional parameter (p): {p}")

# Print the adjacency matrix
# print("Adjacency matrix:")
# for row in adj_matrix:
#     print(row)

# Compute shortest paths using Dijkstra's algorithm
sources = list(range(n))
graph = dijkstra(n, adj_matrix, sources)

# Print the shortest paths
print("Shortest paths:")
# for row in graph:
#     print(row)




# for row in graph:
#     print(row)
print("###########################################################################")

# Extract unique distances
unique_distances = set()
for i in range(len(graph)):
    for j in range(len(graph[i])):
        if graph[i][j] != 0:
            unique_distances.add(graph[i][j])
distinct_distances = sorted(list(unique_distances))

# Define variables
all_Nodes = range(n)
index_z_k = range(len(distinct_distances))
rho = distinct_distances

constraints = WCNF()
top_id = 0

# Variable mappings
y_vars = [j + 1 for j in all_Nodes]
z_vars = [k + n + 1 for k in index_z_k]
top_id = max(z_vars)

print("Variable mappings:")
print("z_vars:", z_vars)
print("y_vars:", y_vars)

# Adding soft constraints
# maximize the (1-z_k) 
for k in index_z_k:
    weight = rho[k]
    clause = [-z_vars[k]]
    constraints.append(clause, weight)
################################                                       
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

# print("Constraints (WCNF):")
# for clause in constraints.hard:
#     print(clause)
# print("Soft constraints:")
# for weight, clause in zip(constraints.wght, constraints.soft):
#     print(weight, clause)

with RC2(constraints, solver="cadical153") as solver:
    for model in solver.enumerate():
        print('Model has cost:', solver.cost)
        # print('Model:', model)
        # print("Values for y_j:")
        # for j in all_Nodes:
        #     print(f"y_{j+1} = {1 if model[y_vars[j] - 1] > 0 else 0}")
        # print("Values for z_k:")
        # for k in index_z_k:
        #     print(f"z_{k+1} = {1 if model[z_vars[k] - 1] > 0 else 0}")
        break
