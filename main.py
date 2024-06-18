from pysat.formula import *
from pysat.pb import EncType as pbenc
from pysat.pb import *
from pysat.card import *
from pysat.solvers import *
from pysat.examples.rc2 import RC2
from pysat.formula import WCNF
import sys

def dijkstra(vertices, graph, src):
    import heapq

    # Initialize distances with infinity and set the distance to src as 0
    dist = [float('inf')] * vertices
    dist[src] = 0

    # Priority queue to store vertices and their distances
    pq = [(0, src)]  # (distance, vertex)

    while pq:
        current_dist, u = heapq.heappop(pq)

        # If current distance is greater than the recorded distance, skip
        if current_dist > dist[u]:
            continue

        # Traverse neighbors of u
        for v in range(vertices):
            if graph[u][v] > 0:  # Only consider non-zero edges
                new_dist = dist[u] + graph[u][v]

                # If found shorter path to v, update distance and push to priority queue
                if new_dist < dist[v]:
                    dist[v] = new_dist
                    heapq.heappush(pq, (new_dist, v))

    # Print the distances from src to all vertices
    print("Vertex \t Distance from Source")
    for node in range(vertices):
        print(node, "\t\t", dist[node])

# Driver program

V = 5
graph = [
    [0, 25, 30, 0, 0],   # A (index 0)
    [25, 0, 0, 10, 0],   # 1 (index 1)
    [30, 0, 0, 15, 5],   # 2 (index 2)
    [0, 10, 15, 0, 15],  # 3 (index 3)
    [0, 0, 5, 15, 0]     # 4 (index 4)
]
src = 0
# dijkstra(V, graph, src)

    
# constraints = WCNF()
# # def var_index(i, j, k):
# #     return (i-1)*slots *length_of_paper_range  + (c-1)*length_of_paper_range + l

# # def var_x(s, c, l):
# #     return (s-1)*slots *length_of_paper_range  + (c-1)*length_of_paper_range + l

# print (len(graph)-len(src))