from pysat.formula import *
from pysat.pb import EncType as pbenc
from pysat.pb import *
from pysat.card import *
from pysat.solvers import *
from pysat.examples.rc2 import RC2
from pysat.formula import WCNF
import sys
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

V = 5
graph = [
    [0, 25, 30, 0, 0],   # A (index 0)
    [25, 0, 0, 10, 0],   # 1 (index 1)
    [30, 0, 0, 15, 5],   # 2 (index 2)
    [0, 10, 15, 0, 15],  # 3 (index 3)
    [0, 0, 5, 15, 0]     # 4 (index 4)
]
sources = [0,1,2]  # Sources as a list of indices

dijkstra(V, graph, sources)
############################distict distance of the matrix####################################################################
# Use a set to store unique distances
unique_distances = set()

# Iterate through the matrix
for i in range(len(graph)):
    for j in range(len(graph[i])):
        if graph[i][j] != 0:
            unique_distances.add(graph[i][j])

# Convert the set to a sorted list
distinct_distances = sorted(list(unique_distances))
nbrDistinctDistances = len(distinct_distances)
print (distinct_distances)
############################################################################################################################


    
constraints = WCNF()
nbrDemandNodes=V-len(sources)
nbrFacilityNodes=len(sources)   
# def var_a_ijk(i, j, k):
#     return (i-1)*nbrFacilityNodes *nbrDistinctDistances  + (j-1)*nbrDistinctDistances + k
# Total number of variables for a_ijk
total_a_ijk_vars = nbrDemandNodes * nbrFacilityNodes * nbrDistinctDistances

# Function to get the variable number for a_ijk
def var_a_ijk(i, j, k):
    return (i * nbrFacilityNodes * nbrDistinctDistances) + (j * nbrDistinctDistances) + k + 1

# Function to get the variable number for y_j
def var_y_j(j):
    return total_a_ijk_vars + j + 1

# Function to get the variable number for z_k
def var_z_k(k):
    return total_a_ijk_vars + nbrFacilityNodes + k + 1

for i in range()


