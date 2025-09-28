# Step 1: Import necessary libraries
import numpy as np
import matplotlib.pyplot as plt

# Step 2: Define simulation parameters for TLC NAND
# These values are based on the project plan.
num_cells = 10000          # The total number of cells in our memory block
mean_endurance = 3000      # The average P/E cycles a TLC cell can handle before failure
std_dev = 300              # The standard deviation, representing manufacturing variations

# Step 3: Generate the endurance thresholds for each cell
# We'll use a normal (Gaussian) distribution to model the cell-to-cell variation.
# Each cell gets a unique endurance value sampled from this distribution.
# We also convert the values to integers since P/E cycles are whole numbers.
cell_endurance_thresholds = np.random.normal(loc=mean_endurance, scale=std_dev, size=num_cells).astype(int)

# Step 4: Visualize the distribution with a histogram
# This plot confirms that our cell generation logic is working correctly.
plt.figure(figsize=(10, 6))  # Set the figure size for better readability
plt.hist(cell_endurance_thresholds, bins=50, edgecolor='black')

# Add labels and a title for clarity
plt.title('Distribution of NAND Cell Endurance Thresholds', fontsize=16)
plt.xlabel('Program/Erase (P/E) Cycles Until Failure', fontsize=12)
plt.ylabel('Number of Cells', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)

# Display the plot
plt.show()

# Optional: Print some sample data to see the generated values
print("Generated Endurance Thresholds (first 10 cells):")
print(cell_endurance_thresholds[:10])

print(f"\nAverage endurance of generated cells: {cell_endurance_thresholds.mean():.2f}")