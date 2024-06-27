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

def solve_p_center(dist_matrix, p):
    n = len(dist_matrix)
    mdl = Model('p-center')

    # Variables
    y = mdl.binary_var_list(n, name='y')
    x = mdl.binary_var_matrix(n, n, name='x')
    z = mdl.continuous_var(name='z')

    # Objective
    mdl.minimize(z)

    # Constraints
    for i in range(n):
        mdl.add_constraint(mdl.sum(dist_matrix[i][j] * x[i, j] for j in range(n)) <= z)
        mdl.add_constraint(mdl.sum(x[i, j] for j in range(n)) == 1)
        for j in range(n):
            mdl.add_constraint(x[i, j] <= y[j])

    mdl.add_constraint(mdl.sum(y[j] for j in range(n)) == p)

    # Solve the model
    solution = mdl.solve()

    if solution:
        centers = [j for j in range(n) if y[j].solution_value > 0.5]
        max_distance = z.solution_value
        # Print y and x variables with adjusted counters
        y_values = {j: y[j].solution_value for j in range(n)}
        x_values = {(i, j): x[i, j].solution_value for i in range(n) for j in range(n)}

        print("Centers placed at indices:", [j+1 for j in centers])
        print("Maximum distance to nearest center:", max_distance)
        print("Values for y_j:")
        for j in range(n):
            print(f"y_{j+1} = {y_values[j]}")
        print("Values for x_ij:")
        for i in range(n):
            for j in range(n):
                print(f"x_{i+1},{j+1} = {x_values[(i, j)]}")

        return centers, max_distance, y_values, x_values
    else:
        print("No optimal solution found.")
        return None, None, None, None

# Example usage
nbrNodes = 3
g = [
    [0, 25, 15],  
    [25, 0, 5],   
    [15, 5, 0],       
]
p = 1
sources = list(range(nbrNodes))
graph = dijkstra(nbrNodes, g, sources)

centers, max_distance, y_values, x_values = solve_p_center(graph, p)
