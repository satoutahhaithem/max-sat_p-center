from docplex.mp.model import Model
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
V = 3

g = [
    [0, 25, 0],  
    [10, 0, 20],   
    [15, 5, 0],       
]
# g = [
#     [0, 25, 30, 0, 0],   # A (index 0)
#     [25, 0, 0, 10, 0],   # 1 (index 1)
#     [30, 0, 0, 15, 5],   # 2 (index 2)
#     [0, 10, 15, 0, 15],  # 3 (index 3)
#     [0, 0, 5, 15, 0]     # 4 (index 4)
# ]

sources = list(range(V)) 
graph = dijkstra(V, g, sources)
for row in graph:
    print (row)
print("###########################################################################")

p = 2   # Example limit for the sum of y_j
unique_distances = set()

# Iterate through the matrix
for i in range(len(graph)):
    for j in range(len(graph[i])):
        if graph[i][j] != 0:
            unique_distances.add(graph[i][j])

# Convert the set to a sorted list
distinct_distances = sorted(list(unique_distances))
print (distinct_distances)

# Define the parameters of the model
# Note: These values should be set according to your specific problem instance
# M = range(5) 
# T = range(4)
# N = range(3) 
# rho = [1, 2, 3, 4]  # Example costs for z_k
# a = [[[1, 0, 1, 0],
#       [0, 1, 0, 1],
#       [1, 1, 0, 0],
#       [0, 0, 1, 1],
#       [1, 0, 0, 1]],  # Example matrix for a_ijk
#      [[0, 1, 1, 0],
#       [1, 0, 0, 1],
#       [0, 1, 0, 0],
#       [1, 0, 1, 1],
#       [0, 0, 0, 1]],
#      [[1, 0, 0, 0],
#       [0, 1, 1, 1],
#       [1, 0, 0, 1],
#       [0, 0, 1, 0],
#       [1, 1, 0, 0]]]



M = range(V)  # Example set of indices for y_j
T = range(len(distinct_distances))  # Example set of indices for z_k
N = range(V)  # Example set of indices for i
rho = distinct_distances  # Example costs for z_k

# a = []
# for k in range(len(distinct_distances)):
#     a_k = []
#     for i in range(V):
#         a_i = []
#         for j in range(V):
#             if graph[i][j] <= distinct_distances[k] and graph[i][j] != 0:
#                 a_i.append(1)
#             else:
#                 a_i.append(0)
#         a_k.append(a_i)
#     a.append(a_k)
# for k in range(len(distinct_distances)):
#     print(f"a_ijk for rho_{k} = {distinct_distances[k]}:")
#     for i in range(V):
#         print(a[k][i])
#     print()


# Create a model
mdl = Model(name='CalikModel')

# Define decision variables
y = mdl.binary_var_list(M, name='y')
z = mdl.binary_var_list(T, name='z')

# Define the objective function
mdl.minimize(mdl.sum(rho[k] * z[k] for k in T))

# # Define the constraints
# for k in T:
#     for i in N:
#         mdl.add_constraint(mdl.sum(a[i][j][k] * y[j] for j in M) >= z[k])
for i in N:
    for k in T : 
         for j in range(V):
            if graph[i][j] <= distinct_distances[k] and graph[i][j] != 0:
                mdl.add_constraint(mdl.sum(y[j]) >= z[k])

mdl.add_constraint(mdl.sum(y[j] for j in M) <= p)

mdl.add_constraint(mdl.sum(z[k] for k in T) == 1)

# Solve the model
solution = mdl.solve(log_output=True)

# Display the solution
if solution:
    print("Solution status:", solution.solve_status)
    print("Objective value:", solution.objective_value)
    print("Values for y_j:")
    for j in M:
        print(f"y_{j} = {y[j].solution_value}")
    print("Values for z_k:")
    for k in T:
        print(f"z_{k} = {z[k].solution_value}")
else:
    print("No solution found")
