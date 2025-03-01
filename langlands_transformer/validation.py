def check_critical_line(sigma_list, tolerance=1e-6):
    deviations = [abs(sigma - 0.5) for sigma in sigma_list]
    return max(deviations) < tolerance
