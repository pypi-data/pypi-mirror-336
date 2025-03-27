import numpy as np

def Scott(x):
    n = len(x)
    std_dev = np.std(x)
    scott_factor = 3.5 / (n ** (1 / 3))
    bandwidth = scott_factor * std_dev
    return bandwidth
