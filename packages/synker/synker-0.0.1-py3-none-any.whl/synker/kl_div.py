import numpy as np
from .kde import KDE_2D

def KL_div(real_data, synthetic_data, hx, hy, eps=1e-10):
    """
    Compute KL divergence between real data and synthetic data using custom KDE.

    Args:
        real_data: 2D array with real data points (first column for X, second for Y).
        synthetic_data: 2D array with synthetic data points (first column for X, second for Y).
        hx: Bandwidth for the X variable.
        hy: Bandwidth for the Y variable.
        eps: Small constant to avoid division by zero and log(0).

    Returns:
        kl_divergence_value: The KL divergence between the real and synthetic data distributions.
    """
    # Generate a grid of points for evaluation
    grid_x = np.linspace(min(real_data[:, 0].min(), synthetic_data[:, 0].min()), 
                          max(real_data[:, 0].max(), synthetic_data[:, 0].max()), 
                          10)
    grid_y = np.linspace(min(real_data[:, 1].min(), synthetic_data[:, 1].min()), 
                          max(real_data[:, 1].max(), synthetic_data[:, 1].max()), 
                          10)
    
    # Compute KDE for real and synthetic data using the custom kde function
    real_density = KDE_2D(real_data[:, 0], real_data[:, 1], grid_x, grid_y, hx, hy)
    synthetic_density = KDE_2D(synthetic_data[:, 0], synthetic_data[:, 1], grid_x, grid_y, hx, hy)
    
    # Normalize the densities to create proper probability distributions
    real_density /= real_density.sum()
    synthetic_density /= synthetic_density.sum()

    # Add a small value (epsilon) to avoid division by zero or log of zero
    real_density += eps
    synthetic_density += eps

    # Calculate KL divergence while avoiding invalid values
    kl_divergence_value = np.sum(real_density * np.log(real_density / synthetic_density))

    return kl_divergence_value