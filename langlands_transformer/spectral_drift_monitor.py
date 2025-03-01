import numpy as np

class SpectralDriftMonitor:
    """
    Tracks spectral drift across time using the Spectral Drift Index (SDI).

    SDI = (1/N) * sum |sigma - 0.5|
    This measures the average deviation from the critical line.

    If SDI exceeds a specified threshold, the monitor flags potential structural drift.
    """

    def __init__(self, drift_threshold=0.05):
        """
        Initialize the drift monitor.

        Parameters:
        - drift_threshold (float): Maximum allowed average deviation from the critical line.
        """
        self.history = []  # Historical SDI values across different time steps
        self.drift_threshold = drift_threshold

    def compute_sdi(self, sigma_list):
        """
        Compute the Spectral Drift Index (SDI) for a given set of spectral values.

        Parameters:
        - sigma_list (list of float): Spectral embeddings (usually between 0 and 1).

        Returns:
        - float: The computed Spectral Drift Index.
        """
        deviations = [abs(sigma - 0.5) for sigma in sigma_list]
        sdi = np.mean(deviations)
        self.history.append(sdi)
        return sdi

    def check_drift(self, sigma_list):
        """
        Check for excessive spectral drift using the SDI and drift threshold.

        Parameters:
        - sigma_list (list of float): Current set of spectral embeddings.

        Returns:
        - bool: True if drift exceeds the threshold, False otherwise.
        """
        sdi = self.compute_sdi(sigma_list)
        if sdi > self.drift_threshold:
            print(f"Warning: Spectral Drift Index ({sdi:.5f}) exceeds threshold ({self.drift_threshold:.5f}).")
            return True
        return False

    def plot_drift_over_time(self):
        """
        Plot the historical evolution of the Spectral Drift Index.
        """
        import matplotlib.pyplot as plt

        plt.plot(self.history, marker='o', linestyle='-', color='royalblue')
        plt.axhline(self.drift_threshold, color='red', linestyle='--', label='Drift Threshold')
        plt.xlabel('Time Step')
        plt.ylabel('Spectral Drift Index (SDI)')
        plt.legend()
        plt.title('Spectral Drift Over Time')
        plt.show()
