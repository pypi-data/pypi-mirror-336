import numpy as np
from synker.kde import KDE_2D

def Synthetic(real_data, hx, hy, grid_x, grid_y, n_samples=None):
    """
    Generate synthetic data based on the Kernel Density Estimation (KDE).

    Args:
        real_data: 2D array with real data points (first column for X, second for Y).
        hx: Bandwidth for the X variable.
        hy: Bandwidth for the Y variable.
        grid_x: Grid points for the X axis.
        grid_y: Grid points for the Y axis.
        n_samples: Number of synthetic samples to generate (default = len(real_data)).

    Returns:
        Synthetic data generated using KDE.
    """
    # Use KDE to estimate the joint density of the real data
    density = KDE_2D(real_data[:, 0], real_data[:, 1], grid_x, grid_y, hx, hy)

    # Normalize the density to ensure it sums to 1
    density /= density.sum()

    # Flatten the density for sampling
    flattened_density = density.flatten()

    # Determine the number of samples to generate
    if n_samples is None:
        n_samples = len(real_data)

    # Normalize probabilities for grid_x and grid_y
    prob_x = density.sum(axis=1) / density.sum()  # Sum across rows for grid_x
    prob_y = density.sum(axis=0) / density.sum()  # Sum across columns for grid_y

    # Generate synthetic samples by sampling from the KDE
    synthetic_data = np.column_stack([
        np.random.choice(grid_x, size=n_samples, p=prob_x),
        np.random.choice(grid_y, size=n_samples, p=prob_y)
    ])

    return synthetic_data
