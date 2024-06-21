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
    [15, 0, 0],     
]
p=2
sources = list(range(nbrNodes)) 
graph = dijkstra(nbrNodes, g, sources)
for row in graph:
    print (row)
print("###########################################################################")

# Extract unique distances from the graph
unique_distances = set()
for i in range(nbrNodes):
    for j in range(i + 1, nbrNodes):
        if graph[i][j] != 0:
            unique_distances.add(graph[i][j])

# Convert set to sorted list
distinct_distances = sorted(list(unique_distances))
all_Nodes = range(1, nbrNodes + 1)  # Indices for y_j (vertices)
index_z_k = range(1, len(distinct_distances) + 1)  # Indices for z_k (radii)
y_vars = [j  for j in all_Nodes]
for k in index_z_k:
    inter=k + nbrNodes
    z_vars = [inter]