import matplotlib.pyplot as plt

def plot_spectral_distribution(sigma_list):
    plt.hist(sigma_list, bins=30, alpha=0.75, color='blue', edgecolor='black')
    plt.axvline(0.5, color='red', linestyle='--', label="Critical Line")
    plt.xlabel("Spectral Value (σ)")
    plt.ylabel("Density")
    plt.legend()
    plt.title("Spectral Distribution of L-function Zeros")
    plt.show()
