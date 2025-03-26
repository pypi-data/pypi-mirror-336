import numpy as np

def KDE_2D(x, y, xi, yi, hx, hy):
    """
    Kernel Density Estimation (KDE) for joint distribution of 2D data.

    Args:
        x: Array of x data points.
        y: Array of y data points.
        xi: Grid points for x-axis.
        yi: Grid points for y-axis.
        hx: Bandwidth for x (T).
        hy: Bandwidth for y (Hs).

    Returns:
        2D density array for the joint distribution.
    """
    x = np.asarray(x)
    y = np.asarray(y)
    xi = np.asarray(xi)
    yi = np.asarray(yi)

    if x.ndim != 1 or y.ndim != 1 or xi.ndim != 1 or yi.ndim != 1:
        raise ValueError("Input arrays must be 1D.")
    if len(x) != len(y):
        raise ValueError("x and y must have the same length.")
    if hx <= 0 or hy <= 0:
        raise ValueError("Bandwidths hx and hy must be positive.")

    n = len(x)
    p = np.zeros((len(xi), len(yi)))

    for i in range(n):
        p1 = np.exp(-((x[i] - xi) ** 2) / (2 * hx ** 2))
        p2 = np.exp(-((y[i] - yi) ** 2) / (2 * hy ** 2))
        p += (1 / (n * hx * hy)) * p1[:, np.newaxis] * p2[np.newaxis, :]

    return p