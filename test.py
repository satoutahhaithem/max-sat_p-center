from pysat.formula import WCNF
from pysat.card import CardEnc
from pysat.examples.rc2 import RC2
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

# Define the problem
V = 5  # Number of nodes
graph = [
    [0, 25, 30, 0, 0],   # A (index 0)
    [25, 0, 0, 10, 0],   # 1 (index 1)
    [30, 0, 0, 15, 5],   # 2 (index 2)
    [0, 10, 15, 0, 15],  # 3 (index 3)
    [0, 0, 5, 15, 0]     # 4 (index 4)
]
sources = [0, 1, 2]  # Facility nodes

# Compute shortest distances from sources using Dijkstra
distances = dijkstra(V, graph, sources)
unique_distances = sorted({graph[i][j] for i in range(V) for j in range(V) if graph[i][j] != 0})
nbrDistinctDistances = len(unique_distances)

# Initialize WCNF formula
constraints = WCNF()
nbrDemandNodes = V - len(sources)
nbrFacilityNodes = len(sources)
p = 2  # Maximum number of facility nodes to select

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

# Add Vertex Coverage Constraint: sum(a_ijk * y_j + !z_k) >= 1
for i in range(nbrDemandNodes):
    for k in range(nbrDistinctDistances):
        clause = []
        for j in range(nbrFacilityNodes):
            clause.append(var_a_ijk(i, j, k))
        clause.append(-var_z_k(k))
        constraints.append(clause)

# Add Selection of Radii Constraint: sum(z_k) = 1
constraints.extend(CardEnc.equals([var_z_k(k) for k in range(nbrDistinctDistances)], 1))

# Add Binary Restriction: y_j in {0,1} and z_k in {0,1}
for j in range(nbrFacilityNodes):
    constraints.append([var_y_j(j)])
    constraints.append([-var_y_j(j)])

for k in range(nbrDistinctDistances):
    constraints.append([var_z_k(k)])
    constraints.append([-var_z_k(k)])

# Add Objective Function: minimize sum(rho_k * !z_k)
# In WCNF, we represent the objective function using soft clauses
for k, rho_k in enumerate(unique_distances):
    constraints.append([-var_z_k(k)], weight=rho_k)

# Add Center Limitation Constraint: at most p facilities can be selected
constraints.extend(CardEnc.atmost([var_y_j(j) for j in range(nbrFacilityNodes)], p))

# Print the CNF formula (for debugging purposes)
print("Hard Clauses:", constraints.hard)
print("Soft Clauses:", constraints.soft)
print("Weights:", constraints.wght)

# Solve the problem using RC2
solver = RC2(constraints)
solution = solver.compute()

# After solving, print the solution details
if solution:
    print("Solution found:", solution)
    # Further analysis of the solution can be added here
    for var in solution:
        if var > 0:
            if var <= total_a_ijk_vars:
                i = (var - 1) // (nbrFacilityNodes * nbrDistinctDistances)
                j = ((var - 1) % (nbrFacilityNodes * nbrDistinctDistances)) // nbrDistinctDistances
                k = (var - 1) % nbrDistinctDistances
                print(f"a_ijk: demand node {i}, facility node {j}, distance index {k} is True")
            elif var <= total_a_ijk_vars + nbrFacilityNodes:
                j = var - total_a_ijk_vars - 1
                print(f"y_j: facility node {j} is True")
            else:
                k = var - total_a_ijk_vars - nbrFacilityNodes - 1
                print(f"z_k: distance index {k} is True")

    # Further analysis of the solution can be added here

else:
    print("No solution found.")
