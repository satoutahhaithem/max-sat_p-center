from docplex.mp.model import Model
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

# Example graph
V = 3
g = [
    [0, 25, 15],  
    [25, 0, 5],   
    [15, 5, 0],       
]

sources = list(range(V))
graph = dijkstra(V, g, sources)

p = 1
unique_distances = set()
for i in range(len(graph)):
    for j in range(len(graph[i])):
        if graph[i][j] != 0:
            unique_distances.add(graph[i][j])
distinct_distances = sorted(list(unique_distances))

M = range(V)  # Indices for y_j
T = range(len(distinct_distances))  # Indices for z_k
N = range(V)  # Indices for i
rho = distinct_distances  # Costs for z_k

mdl = Model(name='p-center')

# Define decision variables
y = mdl.binary_var_list(M, name='y')
z = mdl.binary_var_list(T, name='z')

# Define the objective function
mdl.maximize(mdl.sum(rho[k] * z[k] for k in T))

# Constraints
for i in N:
    for k in T:
        mdl.add_constraint(mdl.sum(y[j] for j in M if graph[i][j] <= rho[k] and graph[i][j] != 0) >= z[k])

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
        print(f"y_{j+1} = {y[j].solution_value}")
    print("Values for z_k:")
    for k in T:
        print(f"z_{k+1} = {z[k].solution_value}")
else:
    print("No solution found")
