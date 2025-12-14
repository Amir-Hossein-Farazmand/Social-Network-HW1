import networkx as nx
import numpy as np
from scipy import stats

def analyze_critical_state(N=10000, num_bins=15):

    # Generate Network at critical state
    p = 1 / (N - 1)
    G = nx.fast_gnp_random_graph(N, p)
    
    # Get Component Sizes
    comp_sizes = [len(c) for c in nx.connected_components(G)]
    comp_sizes = np.array(comp_sizes)
    
    # Logarithmic Binning
    min_size = 1
    max_size = max(comp_sizes)
    bins = np.logspace(np.log10(min_size), np.log10(max_size), num=num_bins)
    

    counts, bin_edges = np.histogram(comp_sizes, bins=bins, weights=comp_sizes)
    
    # Calculate bin widths
    bin_widths = np.diff(bin_edges)
    

    # Density = count / (N * bin_width)
    pdf_values = counts / (N * bin_widths)
    
    # Calculate bin centers
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    
    # Filter empty bins
    valid = pdf_values > 0
    x = bin_centers[valid]
    y = pdf_values[valid]
    
    # Estimate Alpha
    log_x = np.log10(x)
    log_y = np.log10(y)
    slope, intercept, _, _, _ = stats.linregress(log_x, log_y)
    alpha = -slope
    
    print(f"Largest component: {max_size}")
    print(f"Estimated Alpha: {alpha:.4f}")
    
    return x, y, alpha