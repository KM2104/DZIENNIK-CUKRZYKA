# 🏗️ Budowanie Aplikacji Health Monitor jako .EXE

## 📋 Wymagania

- Python 3.8 lub nowszy
- Zainstalowane zależności z `requirements.txt`
- PyInstaller (zostanie automatycznie zainstalowany)

## 🚀 Jak zbudować aplikację?

### Metoda 1: Używając skryptu BAT (ZALECANE - Windows)

1. Kliknij dwukrotnie na plik: **`BUILD_EXE.bat`**
2. Poczekaj aż proces się zakończy
3. Gotowy plik znajdziesz w: `src/dist/HealthMonitor.exe`

### Metoda 2: Ręcznie przez terminal

```bash
# Aktywuj środowisko wirtualne (jeśli używasz)
.venv\Scripts\activate

# Uruchom skrypt budowania
python build_exe.py
```

## 📦 Co się dzieje podczas budowania?

1. ✓ Sprawdzenie i instalacja PyInstaller (jeśli potrzebna)
2. ✓ Czyszczenie poprzednich buildów
3. ✓ Kompilacja aplikacji do pojedynczego pliku .exe
4. ✓ Dołączenie wszystkich zależności (Kivy, Matplotlib, ReportLab)
5. ✓ Utworzenie aplikacji standalone bez konsoli

## 🎯 Cechy aplikacji .EXE

### ✅ Portable (Przenośna)

- **Jeden plik** - wszystko w HealthMonitor.exe
- **Brak instalacji** - wystarczy skopiować i uruchomić
- **Przenośna baza danych** - tworzona w katalogu z .exe
- **Lokalne backupy** - zapisywane obok aplikacji

### 📁 Struktura danych

Gdy uruchomisz `HealthMonitor.exe`, automatycznie utworzy:

```
Folder_z_exe/
├── HealthMonitor.exe     ← Aplikacja
├── health.db             ← Baza danych (auto-tworzenie)
├── backups/              ← Backupy (auto-tworzenie)
│   └── health_backup_YYYYMMDD_HHMMSS.db
└── exports/              ← Eksporty CSV/PDF (auto-tworzenie)
    └── nazwa_pliku.csv
```

## 🖥️ Jak używać na różnych komputerach?

### Komputer #1 - Pierwszy użytek:

1. Uruchom `HealthMonitor.exe`
2. Aplikacja utworzy bazę danych `health.db`
3. Wprowadź dane, utwórz użytkowników

### Przenoszenie na Komputer #2:

**OPCJA A - Z danymi:**

1. Skopiuj **cały folder** z .exe i bazą `health.db`
2. Uruchom na nowym komputerze - wszystkie dane będą dostępne

**OPCJA B - Bez danych (czysta instalacja):**

1. Skopiuj tylko `HealthMonitor.exe`
2. Uruchom - aplikacja utworzy nową pustą bazę

### Synchronizacja danych między komputerami:

1. Na komputerze #1: Ustawienia → Backup → Wykonaj backup
2. Skopiuj plik backupu (`.db`) na pendrive
3. Na komputerze #2: Ustawienia → Restore → Przywróć backup

## 🔧 Rozwiązywanie problemów

### Aplikacja nie uruchamia się

- Sprawdź czy masz uprawnienia do uruchamiania .exe
- Wyłącz antywirus tymczasowo (może blokować)
- Uruchom jako Administrator

### Błąd podczas budowania

```bash
# Zainstaluj ponownie zależności
pip install --upgrade -r requirements.txt
pip install --upgrade pyinstaller

# Wyczyść cache Pythona
python -c "import shutil; shutil.rmtree('__pycache__', ignore_errors=True)"

# Spróbuj ponownie
python build_exe.py
```

### Aplikacja duża (>100 MB)

To normalne - zawiera:

- Kompletny Python runtime
- Kivy framework
- Matplotlib
- ReportLab
- Wszystkie biblioteki systemowe

### Chcę mniejszy plik

Możesz użyć UPX do kompresji:

```bash
pip install pyinstaller[encryption]
# Edytuj build_exe.py i dodaj: '--upx-dir=ścieżka_do_upx'
```

## 📝 Dodatkowe opcje buildowania

### Dodanie ikony aplikacji:

1. Przygotuj plik `icon.ico` (rozmiar 256x256)
2. Umieść w folderze `src/`
3. W pliku `build_exe.py` zmień:
   ```python
   '--icon=NONE',  # na:
   '--icon=icon.ico',
   ```

### Włączenie konsoli debug (do testowania):

W pliku `build_exe.py` zmień:

```python
'--windowed',  # na:
'--console',
```

### Build bez jednego pliku (szybsze uruchamianie):

W pliku `build_exe.py` zmień:

```python
'--onefile',  # na:
'--onedir',
```

Wtedy otrzymasz folder `dist/HealthMonitor/` z plikiem .exe i bibliotekami

## 🎨 Customizacja

### Nazwa aplikacji

W `build_exe.py` zmień:

```python
'--name=HealthMonitor',  # na np:
'--name=DziennikZdrowia',
```

### Dodanie plików zasobów

Jeśli masz obrazki, fonty, itp.:

```python
'--add-data=obrazki;obrazki',
'--add-data=czcionki;czcionki',
```

## 📊 Testowanie aplikacji .EXE

1. **Test lokalny:**

   ```
   src/dist/HealthMonitor.exe
   ```

2. **Test przenośności:**

   - Skopiuj na Pulpit
   - Skopiuj na pendrive
   - Skopiuj do innego folderu
   - Każdy powinien działać niezależnie

3. **Test na innym komputerze:**
   - Przenieś tylko .exe
   - Uruchom i sprawdź działanie

## 🆘 Pomoc

Jeśli coś nie działa:

1. Sprawdź logi w konsoli podczas budowania
2. Sprawdź czy wszystkie zależności są zainstalowane
3. Upewnij się że używasz Python 3.8+
4. Sprawdź czy masz wystarczająco miejsca na dysku (min. 500 MB)

## 📄 Licencja i Dystrybucja

- Aplikacja .exe może być swobodnie kopiowana
- Nie wymaga instalacji Pythona na docelowym komputerze
- Działa na Windows 7/8/10/11 (64-bit)
- Zawiera wszystkie potrzebne biblioteki

---

**Autor:** Health Monitor Team  
**Wersja:** 1.0  
**Data:** 2026
