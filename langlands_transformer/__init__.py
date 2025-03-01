from .embedding import spectral_embedding
from .symmetry import enforce_symmetry
from .propagation import spectral_attention
from .validation import check_critical_line
from .visualization import plot_spectral_distribution

def spectral_machine(data):
    sigma_list = []

    for prime, eigenvalue in zip(data['prime'], data['hecke_eigenvalue']):
        sigma = spectral_embedding(prime, eigenvalue)
        reflected_sigmas = enforce_symmetry(sigma)
        sigma_list.extend(reflected_sigmas)

    attention = spectral_attention(sigma_list)

    for _ in range(10):
        sigma_list = np.dot(attention, sigma_list)

    if check_critical_line(sigma_list):
        print("All spectral points concentrate on the critical line.")
    else:
        print("Spectral instability detected — violates critical line condition.")

    plot_spectral_distribution(sigma_list)

    return sigma_list
