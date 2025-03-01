import numpy as np

def spectral_attention(sigma_list):
    n = len(sigma_list)
    attention_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            distance = abs(sigma_list[i] - sigma_list[j])
            attention_matrix[i, j] = np.exp(-distance**2 / 0.1)
    return attention_matrix / attention_matrix.sum(axis=1, keepdims=True)
