import numpy as np


def compute_gini(array):
    """Compute the Gini coefficient of a numpy array."""
    # Convert to numpy array
    array = np.array(array)
    
    # All values must be positive
    if np.amin(array) < 0:
        array -= np.amin(array)
        
    # Avoid division by zero
    if np.sum(array) == 0:
        return 0.0
    
    # Sort
    array = np.sort(array)
    n = len(array)
    
    # Index
    index = np.arange(1, n + 1)
    
    # Gini formula
    return (np.sum((2 * index - n - 1) * array)) / (n * np.sum(array))