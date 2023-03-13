from pulp import *

# Input variables
widths = list(map(float, input("Enter required subroll widths (in cm), separated by space: ").split()))
demands = list(map(float, input("Enter required subroll demands, separated by space: ").split()))
master_roll_width_lb, master_roll_width_ub = map(float, input("Enter lower and upper bounds of master roll width error range (in cm), separated by space: ").split())
master_roll_width = (master_roll_width_lb + master_roll_width_ub) / 2.0

# Define problem
prob = LpProblem("Cutting Stock Problem", LpMinimize)

# Define variables
x = [LpVariable(f"x{i}", lowBound=0, cat='Integer') for i in range(len(demands))]

# Define objective function
prob += lpSum([x[i]*master_roll_width - demands[i]*widths[i] for i in range(len(demands))])

# Define constraints
for i in range(len(demands)):
    prob += demands[i] <= x[i] * master_roll_width * 1.0 / widths[i]

# Solve problem
prob.solve()

# Print results
for i in range(len(demands)):
    print(f"Number of master rolls used for subrolls of width {widths[i]} cm: {round(x[i].value(), 2)}")
print(f"Total waste: {round(value(prob.objective), 2)} cm")

# Print cutting pattern for each master roll
patterns = [[] for _ in range(int(sum([int(x[i].value()) for i in range(len(demands))])))]
for i in range(len(demands)):
    count = int(x[i].value())
    for j in range(count):
        pattern = [widths[i] for _ in range(int(master_roll_width // widths[i]))]
        if master_roll_width % widths[i] != 0:
            pattern.append(master_roll_width % widths[i])
        patterns[j] += pattern
for i, pattern in enumerate(patterns):
    pattern = [round(p, 2) for p in pattern]
    print(f"Pattern for Master Roll {i+1}: {pattern}")
