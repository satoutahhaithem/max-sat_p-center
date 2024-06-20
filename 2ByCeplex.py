from docplex.mp.model import Model

# Define a simplified graph (smaller example)
V = 3
graph = [
    [0, 10, 20],  # A (index 0)
    [10, 0, 15],  # B (index 1)
    [20, 15, 0]   # C (index 2)
]

# Calculate distinct distances (rho)
unique_distances = set()
for i in range(V):
    for j in range(V):
        if graph[i][j] != 0:
            unique_distances.add(graph[i][j])
rho = sorted(list(unique_distances))

# Calculate a_ijk
a = [[[0 for _ in range(len(rho))] for _ in range(V)] for _ in range(V)]
for i in range(V):
    for j in range(V):
        for k in range(len(rho)):
            a[i][j][k] = 1 if graph[i][j] != 0 and graph[i][j] <= rho[k] else 0

# Print a_ijk matrix for debugging
print("Distinct distances (rho):", rho)
print("a_ijk matrix:")
for i in range(V):
    for j in range(V):
        print(f"a_{i}_{j}_k:", a[i][j])

# Initialize Model
mdl = Model(name='p-center')

# Add variables y_j
y = mdl.binary_var_list(V, name='y')

# Add variables z_k
z = mdl.binary_var_list(len(rho), name='z')

# Set objective function: min sum(rho[k] * z_k)
mdl.minimize(mdl.sum(rho[k] * z[k] for k in range(len(rho))))

# Add constraint: Each demand node i must be covered within the selected radius
for i in range(V):
    for k in range(len(rho)):
        mdl.add_constraint(mdl.sum(a[i][j][k] * y[j] for j in range(V)) >= z[k], f"coverage_{i}_{k}")

# Add constraint: The total number of centers is limited (assuming p = 1 for this example)
p = 1
mdl.add_constraint(mdl.sum(y[j] for j in range(V)) == p, "facility_limit")

# Add constraint: Ensure facility A (index 0) is chosen
mdl.add_constraint(y[0] == 1, "facility_A")

# Add constraint: Exactly one radius is selected
mdl.add_constraint(mdl.sum(z[k] for k in range(len(rho))) == 1, "radius_selection")

# Solve the problem with a time limit (e.g., 60 seconds)
solution = mdl.solve(log_output=True)

# Get the solution
if solution:
    print("Solution status:", solution.solve_status)
    print("Objective value:", solution.objective_value)
    y_solution = solution.get_values(y)
    z_solution = solution.get_values(z)

    print("Values for y_j (facility locations):")
    for j, val in enumerate(y_solution):
        print(f"y_{j} =", val)

    print("Values for z_k (selected radii):")
    for k, val in enumerate(z_solution):
        print(f"z_{k} =", val)
else:
    print("No solution found")
    # Write the model to a file for inspection
    mdl.export_as_lp("p-center.lp")
