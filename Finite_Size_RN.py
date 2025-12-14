import networkx as nx
import numpy as np

def run_finite_size_analysis(n_realizations=50):
    """
    Simulates network evolution for different sizes N to observe finite size effects.
    N values: 100, 1000, 10000.
    Returns a dictionary containing results for each N.
    """
    
    # Network sizes to simulate
    N_list = [100, 1000, 10000]
    
    # Define <k> values
    k_region1 = np.arange(0, 0.8, 0.1)
    k_critical = np.arange(0.8, 1.2 + 0.02, 0.02) 
    k_region2 = np.arange(1.3, 5.0 + 0.1, 0.1)
    
    k_values = np.concatenate([k_region1, k_critical, k_region2])
    k_values = np.unique(k_values)
    k_values.sort()
    
    results = {} 
    
    print(f"Finite Size Effect Simulation Started")
    print(f"Sizes to simulate: {N_list}")
    print(f"Realizations per point: {n_realizations}")

    
    
    for N in N_list:
        print(f"\nProcessing N = {N}...", end=" ", flush=True)
        
        avg_S_values = []
        
        for k in k_values:
            # Calculate probability p
            if N > 1:
                p = k / (N - 1)
            else:
                p = 0
            
            temp_S = []
            

            
            for _ in range(n_realizations):
                # Generate ER Graph
                # For N=10000, fast_gnp_random_graph is faster than erdos_renyi_graph
                # In NetworkX, gnp_random_graph == erdos_renyi_graph
                G = nx.fast_gnp_random_graph(N, p)
                
                # Find Giant Component
                if nx.is_empty(G):
                    NG = 0
                else:
                    largest_cc = max(nx.connected_components(G), key=len)
                    NG = len(largest_cc)
                
                S = NG / N
                temp_S.append(S)
            
            avg_S_values.append(np.mean(temp_S))
            
        results[N] = {
            'k': k_values,
            'S': avg_S_values
        }

    
    return results