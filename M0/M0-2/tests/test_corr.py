import unittest
from legacy_corr import calculate_correlation


class TestCorrelation(unittest.TestCase):
    def test_positive(self):
        _, _, _, r = calculate_correlation([1, 2, 3], [2, 4, 6])
        self.assertAlmostEqual(r, 1.0, places=6)

    def test_negative(self):
        _, _, _, r = calculate_correlation([1, 2, 3], [6, 4, 2])
        self.assertAlmostEqual(r, -1.0, places=6)

    def test_zero_variance(self):
        with self.assertRaises(ValueError):
            calculate_correlation([1, 1, 1], [2, 4, 6])


if __name__ == "__main__":
    unittest.main()