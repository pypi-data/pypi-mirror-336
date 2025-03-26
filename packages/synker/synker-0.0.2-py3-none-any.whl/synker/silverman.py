import numpy as np

def Silverman(x):
    """
    Compute the Silverman's method for bandwidth estimation in 1D.

    Args:
        x: Data array.

    Returns:
        Bandwidth value based on Silverman's method.
    """
    n = len(x)
    std_dev = np.std(x)
    silverman_factor = (4 / (3 * n)) ** (1 / 5)
    bandwidth = silverman_factor * std_dev
    return bandwidth
