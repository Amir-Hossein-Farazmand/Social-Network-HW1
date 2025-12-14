import random

def generate_random_genetic_model(b, x, r):
    """
    Generates a network based on the Random Genetic (RG) model.
    b: barcode length (N=2^b)
    x: number of wildcards 'X' per rule
    r: number of rules
    
    Since the prompt asks for Density calculation for a parameter sweep, 
    we will implement the *simulation* of the rules to count edges.
    """
    N = 2**b
    edges = set()
    
    # Pre-generate binaries
    node_binaries = [format(n, f'0{b}b') for n in range(N)]
    
    for _ in range(r):
        # Select x positions for 'X' (wildcards)
        # The remaining b-x positions are fixed bits (0 or 1)

        # Source Pattern
        s_indices = sorted(random.sample(range(b), b - x)) 
        s_pattern = {} 
        for idx in s_indices:
            s_pattern[idx] = random.choice(['0', '1'])
            
        # Destination Pattern
        d_indices = sorted(random.sample(range(b), b - x))
        d_pattern = {}
        for idx in d_indices:
            d_pattern[idx] = random.choice(['0', '1'])
            
        # Find Matches
        sources = []
        destinations = []
        
        for node_idx, binary in enumerate(node_binaries):
            # Check Source
            s_match = True
            for k, val in s_pattern.items():
                if binary[k] != val:
                    s_match = False
                    break
            if s_match: sources.append(node_idx)
            
            # Check Dest
            d_match = True
            for k, val in d_pattern.items():
                if binary[k] != val:
                    d_match = False
                    break
            if d_match: destinations.append(node_idx)
            
        # Add Edges
        for s in sources:
            for d in destinations:
                edges.add((s, d))
                
    # Calculate Density: Actual Edges / Possible Edges 
    actual_edges = len(edges)
    possible_edges = N * N 
    return actual_edges / possible_edges