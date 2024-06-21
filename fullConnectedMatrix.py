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

# Driver program

V = 5
graph = [
    [0, 25, 30, 0, 0],   # A (index 0)
    [25, 0, 0, 10, 0],   # 1 (index 1)
    [30, 0, 0, 15, 5],   # 2 (index 2)
    [0, 10, 15, 0, 15],  # 3 (index 3)
    [0, 0, 5, 15, 0]     # 4 (index 4)
]
sources = list(range(V))  # Sources as a list of all indices

distances = dijkstra(V, graph, sources)

# Print the full distance matrix
# print("Full distance matrix:")
# for row in distances:
#     print(row)
print(distances)

