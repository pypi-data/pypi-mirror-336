import numpy as np
from synker.kde import kde
from synker.scott import Scott
from synker.silverman import Silverman

def Synthetic(X, Y, hx=None, hy=None, res=100, bandwidth_method=None, grid_x=None, grid_y=None):
    # Bandwidth selection
    if bandwidth_method is not None:
        if bandwidth_method.lower() == "scott":
            hx = Scott(X)
            hy = Scott(Y)
        elif bandwidth_method.lower() == "silverman":
            hx = Silverman(X)
            hy = Silverman(Y)
        else:
            raise ValueError("Invalid bandwidth_method. Choose 'Scott' or 'Silverman'.")
    else:
        if hx is None or hy is None:
            raise ValueError("Provide hx and hy or set bandwidth_method.")
    
    # Grid generation if not provided
    if grid_x is None:
        grid_x = np.linspace(min(X), max(X), res)
    if grid_y is None:
        grid_y = np.linspace(min(Y), max(Y), res)

    # Kernel Density Estimation
    pkde = kde(X, Y, grid_x, grid_y, hx, hy)
    pkde /= pkde.sum()

    # Sampling from the KDE
    num_samples = len(X)
    samples = np.zeros((num_samples, 2))
    for i in range(num_samples):
        xi_idx = np.random.choice(range(len(grid_x)), p=pkde.sum(axis=1))
        yi_idx = np.random.choice(range(len(grid_y)), p=pkde[xi_idx] / pkde[xi_idx].sum())
        samples[i, 0] = grid_x[xi_idx]
        samples[i, 1] = grid_y[yi_idx]

    return samples
