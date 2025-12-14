import networkx as nx
import numpy as np
import time

def run_phase_transition_simulation(N=1000, n_realizations=50):
    
    # Define <k> values with variable step size 
    # Non-critical region 1: 0 to 0.8
    k_region1 = np.arange(0, 0.8, 0.1)
    
    # Critical window: 0.8 to 1.2 
    k_critical = np.arange(0.8, 1.2 + 0.02, 0.02)
    
    # Non-critical region 2: 1.3 to 5
    k_region2 = np.arange(1.3, 5.0 + 0.1, 0.1)
    
    # Combine and sort unique values
    k_values = np.concatenate([k_region1, k_critical, k_region2])
    k_values = np.unique(k_values)
    k_values.sort()
    
    print(f"Simulation Started...")
    print(f"Network Size (N): {N}")
    print(f"Realizations per <k>: {n_realizations}")
    print(f"Total steps: {len(k_values)}")

    print(f"{'  <k>':<8} | {'   p   ':<10} | {'no. of Components':<15} | {'   NG   ':<10} | {'   S   ':<10} | {'   <s>   ':<10}")

    
    # Plotting Data Containers
    plot_k = []
    plot_S = []
    plot_s_mean = []

    start_time = time.time()
    
    for k in k_values:
        # Calculate probability p
        if N > 1:
            p = k / (N - 1)
        else:
            p = 0
            
        # Temporary lists k (over 50 realizations)
        run_S = []
        run_s_mean = []
        run_num_comps = []
        run_NG = []
        
        for _ in range(n_realizations):
            # Generate ER Graph
            G = nx.erdos_renyi_graph(N, p)
            
            # Identify connected components
            components = list(nx.connected_components(G))
            comp_sizes = [len(c) for c in components]
            
            # Stats
            num_comps = len(components)
            run_num_comps.append(num_comps)
            
            if not comp_sizes:
                run_S.append(0)
                run_s_mean.append(0)
                run_NG.append(0)
                continue
                
            # Record size of largest component (NG)
            NG = max(comp_sizes)
            S = NG / N
            
            run_NG.append(NG)
            run_S.append(S)
            
            # Calculate average size of remaining small clusters <s>
            comp_sizes.remove(NG) # Remove largest component
            
            if len(comp_sizes) > 0:
                s_mean = np.mean(comp_sizes)
            else:
                s_mean = 0 
                
            run_s_mean.append(s_mean)
        
        # Averaging over realizations 
        avg_S_val = np.mean(run_S)
        avg_s_mean_val = np.mean(run_s_mean)
        avg_num_comps_val = np.mean(run_num_comps)
        avg_NG_val = np.mean(run_NG)
        
        # Print info for k
        print(f"{k:8.2f} | {p:10.6f} | {avg_num_comps_val:17.1f} | {avg_NG_val:10.1f} | {avg_S_val:10.4f} | {avg_s_mean_val:10.4f}")
        
        # Store for Plotting
        plot_k.append(k)
        plot_S.append(avg_S_val)
        plot_s_mean.append(avg_s_mean_val)


    print(f"Simulation completed.")
    
    return plot_k, plot_S, plot_s_mean