"""
Szybki runner testów - bez importowania Kivy
"""

import sys
import os
import unittest

# Dodaj ścieżkę do modułu src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

if __name__ == "__main__":
    # Uruchom tylko testy jednostkowe (bez GUI)
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Znajdź wszystkie testy
    tests = loader.discover(os.path.dirname(__file__), pattern="test_*.py")
    suite.addTests(tests)

    # Uruchom testy
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Zwróć kod wyjścia
    sys.exit(0 if result.wasSuccessful() else 1)
