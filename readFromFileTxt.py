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
filename = 'instances/test.txt'

# Create the adjacency matrix and get additional parameters
adj_matrix, n, e, p = create_adjacency_matrix(filename)

# Print the additional parameters
print(f"Number of nodes: {n}")
print(f"Number of edges: {e}")
print(f"Additional parameter (p): {p}")

# Print the adjacency matrix
print("Adjacency matrix:")
for row in adj_matrix:
    print(row)

# Compute shortest paths using Dijkstra's algorithm
sources = list(range(n))
shortest_paths = dijkstra(n, adj_matrix, sources)

# Print the shortest paths
print("Shortest paths:")
for row in shortest_paths:
    print(row)
