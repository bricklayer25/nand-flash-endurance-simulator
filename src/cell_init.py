import numpy as np
import matplotlib.pyplot as plt

NAND_TYPES = {
    "1": {"name": "SLC (Single-Level Cell)", "mean": 100000, "std_dev": 10000},
    "2": {"name": "MLC (Multi-Level Cell)", "mean": 10000, "std_dev": 1000},
    "3": {"name": "TLC (Triple-Level Cell)", "mean": 3000, "std_dev": 300},
}

def get_simulation_parameters():
    """Gets simulation parameters from the user via an interactive menu."""
    print("--- Configure Your Simulation ---")
    
    # Let the user choose the NAND type
    while True:
        print("Please select a NAND flash type to simulate:")
        for key, value in NAND_TYPES.items():
            print(f"  {key}: {value['name']}")
        
        choice = input("Enter your choice (1, 2, or 3): ")
        if choice in NAND_TYPES:
            selected_nand = NAND_TYPES[choice]
            break
        else:
            print("\n*** Invalid choice. Please try again. ***\n")
            
    # Let the user choose the number of cells
    while True:
        try:
            num_cells_str = input(f"Enter the number of cells to simulate (e.g., 10000): ")
            num_cells = int(num_cells_str)
            if num_cells > 0:
                break
            else:
                print("\n*** Please enter a positive number. ***\n")
        except ValueError:
            print("\n*** Invalid input. Please enter a whole number. ***\n")
            
    print("-" * 33 + "\n")
    return num_cells, selected_nand['mean'], selected_nand['std_dev'], selected_nand['name']

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
num_cells, mean_endurance, std_dev, nand_name = get_simulation_parameters()

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
max_cycles = mean_endurance + (4 * std_dev)

# ---Calculate a dynamic reporting interval to get 10 updates ---
reporting_interval = max(1, max_cycles // 10)
# 'max(1, ...)' ensures the interval is at least 1, preventing errors on very short simulations.
# ---------------------------------------------------------------

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
    
    if cycle % reporting_interval == 0:
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
