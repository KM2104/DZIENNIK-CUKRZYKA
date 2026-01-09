# Changelog

Wszystkie istotne zmiany w projekcie Health Monitor będą dokumentowane w tym pliku.

Format oparty na [Keep a Changelog](https://keepachangelog.com/pl/1.0.0/),
projekt stosuje [Semantic Versioning](https://semver.org/lang/pl/).

## [Unreleased]

### Dodano

- Wieloużytkownikowy system z obsługą PIN
- Rozszerzone limity ciśnienia (wartości minimalne)
- Przycisk zmiany użytkownika w ekranie głównym
- Opisowe podpowiedzi (hint_text) dla wszystkich pól limitów
- Testy dla zarządzania użytkownikami (test_users.py)
- Testy dla rozszerzonych ustawień (test_settings_extended.py)
- Dokumentacja dla GitHub (README, LICENSE, CONTRIBUTING)

### Zmieniono

- Ulepszony interfejs ekranu ustawień z sekcjami
- Rozbudowane limity ciśnienia o wartości minimalne

## [0.2.0] - 2026-01-09

### Dodano

- Monitorowanie glukozy z oznaczeniem pory dnia i relacji do posiłków
- Monitorowanie tętna
- Wykresy dla wszystkich parametrów zdrowotnych
- System alertów z progami ostrzeżeń
- Konfigurowalne limity dla wszystkich parametrów
- Backup i restore bazy danych
- Eksport danych do CSV
- Historia pomiarów z filtrowaniem

### Zmieniono

- Przeprojektowanie interfejsu użytkownika
- Ulepszona walidacja danych wejściowych

## [0.1.0] - 2025-12-15

### Dodano

- Podstawowe monitorowanie wagi i ciśnienia
- Prosta baza danych SQLite
- Ekran logowania z PIN
- Historia pomiarów
- Podstawowe ustawienia aplikacji

[Unreleased]: https://github.com/twoje-konto/health-monitor/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/twoje-konto/health-monitor/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/twoje-konto/health-monitor/releases/tag/v0.1.0
