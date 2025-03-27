import numpy as np
from .kde import kde

def KL_div(real_data, synthetic_data, hx, hy, eps=1e-10):
    grid_x = np.linspace(min(real_data[:, 0].min(), synthetic_data[:, 0].min()), 
                          max(real_data[:, 0].max(), synthetic_data[:, 0].max()), 
                          10)
    grid_y = np.linspace(min(real_data[:, 1].min(), synthetic_data[:, 1].min()), 
                          max(real_data[:, 1].max(), synthetic_data[:, 1].max()), 
                          10)
    real_density = kde(real_data[:, 0], real_data[:, 1], grid_x, grid_y, hx, hy)
    synthetic_density = kde(synthetic_data[:, 0], synthetic_data[:, 1], grid_x, grid_y, hx, hy)
    real_density /= real_density.sum()
    synthetic_density /= synthetic_density.sum()
    real_density += eps
    synthetic_density += eps
    kl_divergence_value = np.sum(real_density * np.log(real_density / synthetic_density))

    return kl_divergence_value

