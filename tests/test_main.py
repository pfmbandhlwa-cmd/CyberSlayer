import unittest
from src.main import run_cyberslayer

class TestCyberSlayer(unittest.TestCase):
    def test_initialization(self):
        """Test that the core system initializes correctly."""
        self.assertTrue(run_cyberslayer())

if __name__ == "__main__":
    unittest.main()