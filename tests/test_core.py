import unittest
import numpy as np
from depositsense.analysis import confidence_interval, least_squares_trend, buffer_cost
from depositsense.bayes import beta_binomial_update
from depositsense.simulation import simulate_net_outflows

class TestDepositSense(unittest.TestCase):
    def test_confidence_interval_contains_mean(self):
        x = [2,3,4,5,6]
        lo, hi = confidence_interval(x)
        self.assertLessEqual(lo, np.mean(x))
        self.assertGreaterEqual(hi, np.mean(x))

    def test_least_squares_slope(self):
        intercept, slope = least_squares_trend([1,3,5,7])
        self.assertAlmostEqual(intercept, 1.0)
        self.assertAlmostEqual(slope, 2.0)

    def test_bayesian_update(self):
        result = beta_binomial_update([1,1,0,0], 2, 8)
        self.assertEqual(result["posterior_alpha"], 4)
        self.assertEqual(result["posterior_beta"], 10)

    def test_buffer_cost_nonnegative(self):
        self.assertGreaterEqual(buffer_cost(10, [2,8,12,15]), 0)

    def test_simulation_shape(self):
        result = simulate_net_outflows([1,2,3], n_sims=100, horizon=10)
        self.assertEqual(result.shape, (100,))

    def test_simulation_stress_deterministic(self):
        a = simulate_net_outflows([1,2,3], n_sims=50, stress=True)
        b = simulate_net_outflows([1,2,3], n_sims=50, stress=True)
        np.testing.assert_array_equal(a,b)

if __name__ == "__main__":
    unittest.main()
