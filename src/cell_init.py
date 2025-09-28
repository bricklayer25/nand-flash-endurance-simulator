import numpy as np
import matplotlib.pyplot as plt

def print_exposition(num_cells, mean_endurance, std_dev):
    """Prints an introductory explanation of the simulation."""
    print("=" * 70)
    print("      NAND Flash Endurance Monte Carlo Simulator")
    print("=" * 70)
    print("\nThis script simulates the wear-out process of a block of NAND flash memory.")
    print(f"It models {num_cells:,} individual cells, each with a unique endurance limit")
    print(f"based on a normal distribution (Mean: {mean_endurance}, Std Dev: {std_dev}).\n")
    
    print("--- Key Concepts ---")
    print(
        "  - P/E Cycle (Program/Erase): The fundamental action of writing and erasing a\n"
        "    NAND cell. This is the primary cause of wear."
    )
    print(
        "  - Endurance: The total number of P/E cycles a cell can withstand before\n"
        "    it is likely to fail and no longer reliably store data."
    )
    print(
        "  - BER (Bit Error Rate): The key metric for memory reliability. It's the ratio\n"
        "    of failed cells to the total number of cells."
    )
    print("    Formula: BER = (Number of Failed Cells) / (Total Number of Cells)\n")
    
    print("The simulation will now begin, applying P/E cycles and tracking the BER...\n")
    
# ===================================================================
# Phase 1: Initialization & Visualization of Thresholds
# ===================================================================

# Define simulation parameters for TLC NAND
num_cells = 10000
mean_endurance = 3000
std_dev = 300

#--------------Exposition-------------------
print_exposition(num_cells, mean_endurance, std_dev)
#-------------------------------------------

# Generate the endurance thresholds for each cell
cell_endurance_thresholds = np.random.normal(loc=mean_endurance, scale=std_dev, size=num_cells).astype(int)

# Visualize the initial distribution with a histogram
plt.figure(figsize=(10, 6))
plt.hist(cell_endurance_thresholds, bins=50, edgecolor='black')
plt.title('Distribution of NAND Cell Endurance Thresholds', fontsize=16)
plt.xlabel('Program/Erase (P/E) Cycles Until Failure', fontsize=12)
plt.ylabel('Number of Cells', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.show() # This will display the histogram first

# ===================================================================
# Phase 2: Core Simulation Loop & Raw Data Output
# ===================================================================

# Define the maximum number of cycles to simulate
max_cycles = 5000

# Initialize an array to track P/E counts for each cell
p_e_counts = np.zeros(num_cells, dtype=int)

# Create a list to store the results (cycle, BER)
results_log = []

print("Starting simulation...")

# The main simulation loop
for cycle in range(1, max_cycles + 1):
    p_e_counts += 1 # Apply wear
    failed_cells_mask = p_e_counts > cell_endurance_thresholds # Check for failures
    num_failed = np.sum(failed_cells_mask) # Count failures
    ber = num_failed / num_cells # Calculate BER
    results_log.append((cycle, ber)) # Log data
    
    if cycle % 500 == 0:
        print(f"Cycle {cycle}/{max_cycles} | Failed Cells: {num_failed} | BER: {ber:.6f}")

print("Simulation finished.")

# Convert results to a NumPy array for easier handling
results_array = np.array(results_log)

# Print the final raw data
print("\n--- Raw BER vs. Cycle Data (Last 10 entries) ---")
print(f"{'Cycle':<10}{'BER':<10}")
print("-" * 20)
for cycle, ber in results_array[-10:]:
    print(f"{int(cycle):<10}{ber:<10.6f}")
