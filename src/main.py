import os
import numpy as np
import matplotlib.pyplot as plt

NAND_TYPES = {
    "1": {"name": "SLC (Single-Level Cell)", "mean": 100000, "std_dev": 10000},
    "2": {"name": "MLC (Multi-Level Cell)", "mean": 10000, "std_dev": 1000},
    "3": {"name": "TLC (Triple-Level Cell)", "mean": 3000, "std_dev": 300},
}
    
def run_simulation(num_cells, mean_endurance, std_dev, nand_name):
    """Runs a single NAND endurance simulation and returns the results."""
    print(f"--- Running simulation for {nand_name} ---")
    
    # Generate the endurance thresholds for each cell
    cell_endurance_thresholds = np.random.normal(loc=mean_endurance, scale=std_dev, size=num_cells).astype(int)

    # Calculate a dynamic simulation length
    max_cycles = mean_endurance + (4 * std_dev)
    reporting_interval = max(1, max_cycles // 10)

    # Initialize arrays
    p_e_counts = np.zeros(num_cells, dtype=int)
    results_log = []

    # The main simulation loop
    for cycle in range(1, max_cycles + 1):
        p_e_counts += 1
        failed_cells_mask = p_e_counts > cell_endurance_thresholds
        num_failed = np.sum(failed_cells_mask)
        ber = num_failed / num_cells
        results_log.append((cycle, ber))
        
        if cycle % reporting_interval == 0:
            print(f"  Cycle {cycle}/{max_cycles} | BER: {ber:.6f}")
    
    print(f"Simulation for {nand_name} complete.\n")
    return np.array(results_log)

def plot_comparison_curves(results_dict):
    """Plots the BER curves for multiple NAND types on a single graph."""
    plt.figure(figsize=(12, 8))
    
    for nand_name, results_array in results_dict.items():
        # Unpack the results array into cycles (x) and BER (y)
        cycles = results_array[:, 0]
        bers = results_array[:, 1]
        plt.plot(cycles, bers, label=nand_name)
        
    # --- IMPORTANT: Use a logarithmic scale for the Y-axis ---
    plt.yscale('log')
    
    plt.title('NAND Flash Endurance Comparison', fontsize=16)
    plt.xlabel('Program/Erase (P/E) Cycles', fontsize=12)
    plt.ylabel('Bit Error Rate (BER) - Log Scale', fontsize=12)
    plt.grid(True, which="both", linestyle='--')
    
    # Define the output directory
    output_dir = 'results'
    
    # Create the directory if it doesn't already exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")
    
    # Save the figure to the specified directory
    output_path = os.path.join(output_dir, 'nand_endurance_comparison.png')
    plt.savefig(output_path, dpi=300)
    print(f"Plot successfully saved to {output_path}")
    
    plt.legend()
    plt.show()

# ===================================================================
# Main Script Logic
# ===================================================================

if __name__ == "__main__":
    # Define a constant for the number of cells to use in all simulations
    NUM_CELLS_TO_SIMULATE = 50000

    # A dictionary to store the results from each simulation
    all_results = {}

    # Loop through each defined NAND type and run a simulation for it
    for key, params in NAND_TYPES.items():
        results = run_simulation(
            num_cells=NUM_CELLS_TO_SIMULATE,
            mean_endurance=params['mean'],
            std_dev=params['std_dev'],
            nand_name=params['name']
        )
        all_results[params['name']] = results
        
    # After all simulations are done, plot the final comparison graph
    plot_comparison_curves(all_results)
