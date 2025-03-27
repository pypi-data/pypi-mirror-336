import numpy as np

def Silverman(x):
    n = len(x) 
    std_dev = np.std(x)  
    silverman_factor = (4 / (3 * n)) ** (1 / 5)
    bandwidth = silverman_factor * std_dev  
    return bandwidth
