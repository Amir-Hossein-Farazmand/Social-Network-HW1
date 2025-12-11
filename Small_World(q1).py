import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

def generate_1d_lattice(n):
    """
    Generates a 1D Ring Lattice (k=2 neighbors).
    """
    return nx.cycle_graph(n)

def generate_2d_lattice(n):
    """
    Generates a 2D Square Lattice with periodic boundary conditions.
    """
    side = int(np.sqrt(n))
    return nx.grid_2d_graph(side, side, periodic=True)

def generate_3d_lattice(n):
    """
    Generates a 3D Cubic Lattice.
    """
    side = int(np.cbrt(n))
    return nx.grid_graph(dim=[side, side, side])

def generate_random_network(n, avg_k=4):
    """
    Generates an Erdos-Renyi random graph with average degree <k>.
    p = <k> / (N - 1)
    """
    if n <= 1:
        return nx.empty_graph(n)
    p = avg_k / (n - 1)
    return nx.erdos_renyi_graph(n, p)
