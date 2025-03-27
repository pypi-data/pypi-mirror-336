import unittest
import numpy as np
import matplotlib.pyplot as plt
from synker.scott import Scott
from synker.silverman import Silverman
from synker.kl_div import KL_div
from synker.synthetic import Synthetic
from synker.kde import kde

class TestSynker(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # Generate sample data once for all tests
        np.random.seed(42)
        cls.data = np.random.weibull(a=10, size=(1000, 2))
        cls.X = np.random.weibull(a=5, size=1000)
        cls.Y = np.random.weibull(a=20, size=1000)

    def test_silverman_bandwidth(self):
        hx = Silverman(self.X)
        hy = Silverman(self.Y)
        self.assertGreater(hx, 0)
        self.assertGreater(hy, 0)
        print(f"Silverman's Bandwidth hx: {hx}, hy: {hy}")

    def test_scott_bandwidth(self):
        hx = Scott(self.X)
        hy = Scott(self.Y)
        self.assertGreater(hx, 0)
        self.assertGreater(hy, 0)
        print(f"Scott's Bandwidth hx: {hx}, hy: {hy}")

    def test_kde(self):
        hx = Scott(self.X)
        hy = Scott(self.Y)
        # Using auto grid generation in kde
        syn_X = np.linspace(min(self.X), max(self.X), 100)
        syn_Y = np.linspace(min(self.Y), max(self.Y), 100)
        pkde = kde(self.X, self.Y, syn_X, syn_Y, hx, hy)
        self.assertTrue(np.all(pkde >= 0))
        print("KDE Probability Matrix: \n", pkde)

    def test_synthetic_manual_bandwidth(self):
        hx = Scott(self.X)
        hy = Scott(self.Y)
        # Generate grids for Synthetic Data
        grid_x = np.linspace(min(self.X), max(self.X), 100)
        grid_y = np.linspace(min(self.Y), max(self.Y), 100)
        # Test Synthetic with manually set bandwidths
        synth_data = Synthetic(X=self.X, Y=self.Y, hx=hx, hy=hy, grid_x=grid_x, grid_y=grid_y, res=100)
        self.assertEqual(synth_data.shape[1], 2)
        print("Synthetic Data with Manual Bandwidth: \n", synth_data)

    def test_synthetic_auto_bandwidth(self):
        # Generate grids for Synthetic Data
        grid_x = np.linspace(min(self.X), max(self.X), 100)
        grid_y = np.linspace(min(self.Y), max(self.Y), 100)
        # Test Synthetic with automatic Scott bandwidth selection
        hx = Scott(self.X)
        hy = Scott(self.Y)
        synth_data = Synthetic(X=self.X, Y=self.Y, hx=hx, hy=hy, grid_x=grid_x, grid_y=grid_y, res=100)
        self.assertEqual(synth_data.shape[1], 2)
        print("Synthetic Data with Auto Scott Bandwidth: \n", synth_data)

    def test_kl_divergence(self):
        # Generate grids for Synthetic Data
        grid_x = np.linspace(min(self.X), max(self.X), 100)
        grid_y = np.linspace(min(self.Y), max(self.Y), 100)
        synth_data = Synthetic(X=self.X, Y=self.Y, hx=Scott(self.X), hy=Scott(self.Y), grid_x=grid_x, grid_y=grid_y, res=100)
        kl_div = KL_div(real_data=self.data, synthetic_data=synth_data, hx=Scott(self.X), hy=Scott(self.Y))
        self.assertTrue(np.isfinite(kl_div))
        print("KL Divergence: ", kl_div)

    def test_plot(self):
        # Generate grids for Synthetic Data
        grid_x = np.linspace(min(self.X), max(self.X), 100)
        grid_y = np.linspace(min(self.Y), max(self.Y), 100)
        # Test plot for synthetic data vs real data
        synth_data = Synthetic(X=self.X, Y=self.Y, hx=Scott(self.X), hy=Scott(self.Y), grid_x=grid_x, grid_y=grid_y, res=100)
        Synth_X, Synth_Y = synth_data[:, 0], synth_data[:, 1]
        plt.figure(figsize=(8, 8), dpi=100)
        plt.scatter(self.X, self.Y, label="Real Data")
        plt.scatter(Synth_X, Synth_Y, label="Synthetic Data", alpha=0.7)
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.legend()
        plt.title("Real vs Synthetic Data")
        plt.close()  # Prevent actual plot during test
        print("Plotting test completed.")

if __name__ == "__main__":
    unittest.main()
