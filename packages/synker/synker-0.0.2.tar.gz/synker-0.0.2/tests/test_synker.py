import unittest
import numpy as np
import inspect
from synker import Scott, KDE_2D, Synthetic, KL_div

class TestSynker(unittest.TestCase):
    
    def setUp(self):
        # Generate Weibull-distributed synthetic real data
        np.random.seed(42)
        size = 500  # Sample size
        
        # Weibull distribution parameters for X and Y
        c_X, scale_X = 2.0, 8.0   # shape and scale for period X
        c_Y, scale_Y = 1.5, 3.0 # shape and scale for wave height Y
        
        X = np.random.weibull(c_X, size) * scale_X
        Y = np.random.weibull(c_Y, size) * scale_Y
        
        self.real_data = np.column_stack((X, Y))

    def test_scott_bandwidth(self):
        hx = Scott(self.real_data[:, 0])
        hy = Scott(self.real_data[:, 1])
        self.assertTrue(hx > 0)
        self.assertTrue(hy > 0)
        print(f"Scott's Bandwidths - hx: {hx}, hy: {hy}")

    def test_kde_and_synthetic_generation(self):
        hx = Scott(self.real_data[:, 0])
        hy = Scott(self.real_data[:, 1])
        
        grid_x = np.linspace(self.real_data[:, 0].min(), self.real_data[:, 0].max(), 20)
        grid_y = np.linspace(self.real_data[:, 1].min(), self.real_data[:, 1].max(), 20)
        
        # Test KDE output shape
        density = KDE_2D(self.real_data[:, 0], self.real_data[:, 1], grid_x, grid_y, hx, hy)
        self.assertEqual(density.shape, (len(grid_x), len(grid_y)))
        self.assertTrue(np.all(density >= 0))

        # Test synthetic data generation
        synthetic_data = Synthetic(self.real_data, hx, hy, grid_x, grid_y)
        self.assertEqual(synthetic_data.shape[1], 2)
        self.assertEqual(synthetic_data.shape[0], 500)  # Adjusted to 500 samples

    def test_kl_divergence(self):
        hx = Scott(self.real_data[:, 0])
        hy = Scott(self.real_data[:, 1])
        
        grid_x = np.linspace(self.real_data[:, 0].min(), self.real_data[:, 0].max(), 20)
        grid_y = np.linspace(self.real_data[:, 1].min(), self.real_data[:, 1].max(), 20)
        
        # Test synthetic data generation
        synthetic_data = Synthetic(self.real_data, hx, hy, grid_x, grid_y)
        
        kl_value = KL_div(self.real_data, synthetic_data, hx, hy)
        print(f"KL Divergence: {kl_value}")
        self.assertTrue(kl_value >= 0)

if __name__ == "__main__":
    unittest.main()

# Print function signature for Synthetic
print(inspect.signature(Synthetic))
