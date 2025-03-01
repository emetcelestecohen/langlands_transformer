import numpy as np

def enforce_symmetry(sigma):
    reflected_sigma = 1 - sigma
    return np.array([sigma, reflected_sigma])
