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

    # Print the distances from each source to all vertices
    for i, src in enumerate(sources):
        print(f"Distances from source {src}:")
        print("Vertex \t Distance")
        for node in range(vertices):
            print(node, "\t\t", dist[i][node])
        print()

# Driver program

V = 3
graph = [
[0, 25, 15],
[25, 0, 5],
[15, 0, 0]
]
sources = [0,1,2]  # Sources as a list of indices

dijkstra(V, graph, sources)
