import numpy as np

def Scott(x):
    """
    Compute the Scott's method for bandwidth estimation in 1D.

    Args:
        x: Data array.

    Returns:
        Bandwidth value based on Scott's method.
    """
    n = len(x)
    std_dev = np.std(x)
    scott_factor = 3.5 / (n ** (1 / 3))
    bandwidth = scott_factor * std_dev
    return bandwidth
