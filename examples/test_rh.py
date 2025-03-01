from langlands_transformer import spectral_machine

data = {
    "prime": [2, 3, 5, 7, 11, 13],
    "hecke_eigenvalue": [0.5, -0.7, 0.2, 0.1, 0.9, -0.3]
}

final_sigma = spectral_machine(data)
print(final_sigma)
