"""
Uruchamia wszystkie testy aplikacji
"""

import sys
import os
import unittest

# Dodaj ścieżkę do modułu src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

# Importuj wszystkie testy
from test_validators import (
    TestWeightValidator,
    TestPressureValidator,
    TestHeartRateValidator,
    TestGlucoseValidator,
)
from test_health_rules import (
    TestWeightAlerts,
    TestPressureAlerts,
    TestHeartRateAlerts,
    TestGlucoseAlerts,
)
from test_database import TestDatabase


def run_all_tests():
    """Uruchamia wszystkie testy"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Dodaj wszystkie testy
    suite.addTests(loader.loadTestsFromTestCase(TestWeightValidator))
    suite.addTests(loader.loadTestsFromTestCase(TestPressureValidator))
    suite.addTests(loader.loadTestsFromTestCase(TestHeartRateValidator))
    suite.addTests(loader.loadTestsFromTestCase(TestGlucoseValidator))

    suite.addTests(loader.loadTestsFromTestCase(TestWeightAlerts))
    suite.addTests(loader.loadTestsFromTestCase(TestPressureAlerts))
    suite.addTests(loader.loadTestsFromTestCase(TestHeartRateAlerts))
    suite.addTests(loader.loadTestsFromTestCase(TestGlucoseAlerts))

    suite.addTests(loader.loadTestsFromTestCase(TestDatabase))

    # Uruchom testy
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Zwróć kod wyjścia
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
