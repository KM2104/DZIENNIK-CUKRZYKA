"""
Szybki runner testów - bez importowania Kivy
Uruchamia wszystkie testy jednostkowe w katalogu tests/
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

    # Uruchom testy z szczegółowym outputem
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Wyświetl podsumowanie
    print("\n" + "=" * 70)
    print(f"Wykonano {result.testsRun} testów")
    print(f"✓ Sukces: {result.testsRun - len(result.failures) - len(result.errors)}")
    if result.failures:
        print(f"✗ Niepowodzenia: {len(result.failures)}")
    if result.errors:
        print(f"✗ Błędy: {len(result.errors)}")
    print("=" * 70)

    # Zwróć kod wyjścia
    sys.exit(0 if result.wasSuccessful() else 1)
