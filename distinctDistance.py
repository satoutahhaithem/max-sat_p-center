graph = [
    [0, 25, 30, 0, 0],   # A (index 0)
    [25, 0, 0, 10, 0],   # 1 (index 1)
    [30, 0, 0, 15, 5],   # 2 (index 2)
    [0, 10, 15, 0, 15],  # 3 (index 3)
    [0, 0, 5, 15, 0]     # 4 (index 4)
]

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
print (distinct_distances)
############################################################################################################################