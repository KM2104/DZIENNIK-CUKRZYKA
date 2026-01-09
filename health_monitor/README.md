# 🏥 Health Monitor - Dziennik Cukrzyka

Kompleksowa aplikacja mobilna do monitorowania parametrów zdrowotnych, stworzona z myślą o osobach z cukrzycą i nie tylko. Aplikacja umożliwia śledzenie glukozy, ciśnienia krwi, tętna oraz wagi z zaawansowanym systemem alertów i wieloużytkownikowym dostępem.

![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![Kivy](https://img.shields.io/badge/Kivy-2.3.1-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Funkcjonalności

### 📊 Monitorowanie Parametrów

- **🩸 Glukoza** - pomiary z oznaczeniem pory dnia i relacji do posiłków
- **💓 Ciśnienie krwi** - ciśnienie skurczowe i rozkurczowe
- **❤️ Tętno** - częstość akcji serca
- **⚖️ Waga** - kontrola masy ciała

### 📈 Wykresy i Historia

- Interaktywne wykresy trendów dla wszystkich parametrów
- Historia pomiarów z możliwością eksportu
- Analiza trendów w czasie

### 🔔 Inteligentne Alerty

- Konfigurowalne progi ostrzeżeń dla każdego parametru
- System 3-poziomowy: norma / ostrzeżenie / niebezpieczeństwo
- Natychmiastowe powiadomienia o nieprawidłowych wartościach

### 👥 Wieloużytkownikowy System

- Obsługa wielu użytkowników z oddzielnymi profilami
- Zabezpieczenie PIN dla każdego użytkownika
- Możliwość zmiany PIN i zarządzania użytkownikami
- Szybkie przełączanie między użytkownikami

### 💾 Backup i Eksport

- Tworzenie kopii zapasowych bazy danych
- Przywracanie danych z backupu
- Export danych do CSV i PDF (planowane)

## 🚀 Instalacja

### Wymagania

- Python 3.11 lub nowszy
- pip (menedżer pakietów Python)

### Kroki instalacji

1. **Sklonuj repozytorium:**

```bash
git clone https://github.com/twoje-konto/health-monitor.git
cd health-monitor
```

2. **Utwórz wirtualne środowisko:**

```bash
python -m venv .venv
```

3. **Aktywuj środowisko:**

Windows:

```bash
.venv\Scripts\activate
```

Linux/Mac:

```bash
source .venv/bin/activate
```

4. **Zainstaluj zależności:**

```bash
pip install -r requirements.txt
```

## 🎮 Uruchomienie

### Desktop (Windows/Linux/Mac)

```bash
cd src
python main.py
```

### Android (za pomocą Buildozer)

```bash
buildozer android debug
buildozer android deploy run
```

## 📁 Struktura Projektu

```
health_monitor/
├── src/                    # Kod źródłowy aplikacji
│   ├── main.py            # Punkt wejścia aplikacji
│   ├── health.kv          # Definicje interfejsu Kivy
│   ├── db/                # Warstwa bazy danych
│   │   ├── database.py    # Operacje na bazie SQLite
│   │   └── __init__.py
│   ├── screens/           # Ekrany aplikacji
│   │   ├── login.py       # Ekran logowania
│   │   ├── home.py        # Ekran główny
│   │   ├── glucose.py     # Ekran glukozy
│   │   ├── pressure.py    # Ekran ciśnienia
│   │   ├── heartrate.py   # Ekran tętna
│   │   ├── weight.py      # Ekran wagi
│   │   ├── settings.py    # Ekran ustawień
│   │   └── *_chart.py     # Wykresy dla parametrów
│   └── utils/             # Narzędzia pomocnicze
│       ├── alerts.py      # System alertów
│       ├── backup.py      # Backup/restore
│       ├── charts.py      # Generowanie wykresów
│       ├── dialogs.py     # Dialogi komunikatów
│       ├── health_rules.py # Reguły zdrowotne
│       ├── settings.py    # Zarządzanie ustawieniami
│       └── validators.py  # Walidacja danych
├── tests/                 # Testy jednostkowe
│   ├── test_database.py   # Testy bazy danych
│   ├── test_users.py      # Testy użytkowników
│   ├── test_settings_extended.py
│   ├── test_validators.py
│   └── test_health_rules.py
├── requirements.txt       # Zależności Python
├── buildozer.spec        # Konfiguracja Buildozer (Android)
├── README.md             # Ten plik
├── LICENSE               # Licencja MIT
└── .gitignore           # Pliki ignorowane przez Git
```

## 🧪 Testowanie

Uruchom wszystkie testy:

```bash
cd tests
python run_all_tests.py
```

Uruchom konkretny test:

```bash
python -m unittest tests.test_database
python -m unittest tests.test_users
```

## ⚙️ Konfiguracja

### Domyślne Limity Zdrowotne

| Parametr                       | Min | Ostrzeżenie | Max    |
| ------------------------------ | --- | ----------- | ------ |
| **Glukoza** (mg/dL)            | 70  | 140         | 50-250 |
| **Ciśnienie skurcz.** (mmHg)   | 90  | 140         | 180    |
| **Ciśnienie rozkurcz.** (mmHg) | 60  | 90          | 120    |
| **Tętno** (bpm)                | 60  | 100         | 40-150 |
| **Waga** (kg)                  | 50  | -           | 150    |

Wszystkie limity można dostosować w ekranie Ustawień.

## 📱 Budowanie na Androida

Aplikacja wykorzystuje Buildozer do tworzenia pakietu APK:

```bash
# Inicjalizacja (pierwszorazowo)
buildozer init

# Budowanie debug APK
buildozer android debug

# Instalacja i uruchomienie na urządzeniu
buildozer android deploy run
```

## 🤝 Współpraca

Chętnie przyjmujemy Pull Requesty! Jeśli chcesz pomóc w rozwoju:

1. Zforkuj repozytorium
2. Stwórz branch z nową funkcjonalnością (`git checkout -b feature/AmazingFeature`)
3. Commituj zmiany (`git commit -m 'Add some AmazingFeature'`)
4. Push do brancha (`git push origin feature/AmazingFeature`)
5. Otwórz Pull Request

### Wytyczne dla współpracowników

- Pisz czytelny kod zgodny z PEP 8
- Dodawaj testy dla nowych funkcjonalności
- Aktualizuj dokumentację
- Dbaj o docstringi w kodzie

## 📝 TODO / Planowane Funkcjonalności

- [ ] Export danych do PDF
- [ ] Synchronizacja z chmurą
- [ ] Przypomnienia o pomiarach
- [ ] Statystyki tygodniowe/miesięczne
- [ ] Integracja z urządzeniami Bluetooth (glukometry, ciśnieniomierze)
- [ ] Tryb ciemny
- [ ] Wielojęzyczność
- [ ] Notatki do pomiarów

## 🐛 Zgłaszanie Błędów

Jeśli znajdziesz błąd, proszę [zgłoś go tutaj](https://github.com/twoje-konto/health-monitor/issues) z następującymi informacjami:

- Opis problemu
- Kroki do reprodukcji
- Oczekiwane zachowanie
- Zrzuty ekranu (jeśli możliwe)
- Środowisko (OS, wersja Python)

## 📄 Licencja

Projekt jest udostępniony na licencji MIT. Zobacz plik [LICENSE](LICENSE) dla szczegółów.

## 👨‍💻 Autor

Stworzone z ❤️ dla osób dbających o swoje zdrowie.

## 🙏 Podziękowania

- [Kivy](https://kivy.org/) - framework do tworzenia aplikacji mobilnych
- [Matplotlib](https://matplotlib.org/) - biblioteka do wykresów
- Społeczność open source za nieocenione wsparcie

---

**Uwaga:** Ta aplikacja nie zastępuje profesjonalnej opieki medycznej. Zawsze konsultuj się z lekarzem w sprawie interpretacji wyników i leczenia.
