import numpy as np
import networkx as nx

def generate_deterministic_scale_free(b):
    """
    Generates a Directed Scale-Free network using the Barabasi & Czegel bit-matching heuristic.
    N = 2^b nodes.
    
    Algorithm:
    For i from 0 to b:
        Source Pattern (Si): i '0's followed by (b-i) 'X's.
        Dest Pattern (Di): i 'X's followed by (b-i) '1's.
        Connect all nodes matching Si to all nodes matching Di.
    """
    N = 2**b
    adj_matrix = np.zeros((N, N), dtype=int)
    
    # Pre-generate all binary strings for nodes 0 to N-1
    node_binaries = [format(n, f'0{b}b') for n in range(N)]
    
    for i in range(b + 1):
        # Si: i zeros ('0') + wildcards
        source_prefix = '0' * i
        
        # Di: wildcards + (b-i) ones ('1')
        dest_suffix = '1' * (b - i)
        
        sources = []
        destinations = []
        
        for idx, binary in enumerate(node_binaries):
            # Check Source Match 
            if binary.startswith(source_prefix):
                sources.append(idx)
            
            # Check Dest Match 
            if binary.endswith(dest_suffix):
                destinations.append(idx)
        
        if sources and destinations:
            # block assignment:
            adj_matrix[np.ix_(sources, destinations)] = 1
            
    # Convert to NetworkX DiGraph
    G = nx.from_numpy_array(adj_matrix, create_using=nx.DiGraph)
    return G, adj_matrix

