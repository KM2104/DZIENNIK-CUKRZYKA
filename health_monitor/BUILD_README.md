# 🏗️ SZYBKI PRZEWODNIK - Budowanie .EXE

## ✅ APLIKACJA GOTOWA!

Plik .EXE został już zbudowany i znajduje się w:

```
src/dist/HealthMonitor.exe
```

**Rozmiar:** ~135 MB | **Status:** ✅ Gotowy do użycia

---

## 🚀 DLA UŻYTKOWNIKA - JAK UŻYWAĆ?

### Opcja 1: Uruchom z obecnego miejsca

```
1. Przejdź do: src/dist/
2. Kliknij dwukrotnie: HealthMonitor.exe
3. Gotowe!
```

### Opcja 2: Skopiuj w inne miejsce

```
1. Skopiuj plik: src/dist/HealthMonitor.exe
2. Wklej go gdzie chcesz:
   - Pulpit
   - Pendrive
   - Inny komputer
3. Kliknij dwukrotnie
4. Gotowe!
```

📖 **Szczegóły:** Zobacz plik `src/dist/JAK_UZYWAC.md`

---

## 🔧 DLA DEWELOPERA - JAK ZBUDOWAĆ PONOWNIE?

### Metoda 1: Automatyczna (ZALECANE)

```batch
# Kliknij dwukrotnie na:
BUILD_EXE.bat
```

### Metoda 2: Przez terminal

```bash
# Aktywuj środowisko wirtualne
.venv\Scripts\activate

# Uruchom build
python build_exe.py
```

### Metoda 3: Ręcznie z PyInstaller

```bash
cd src
pyinstaller --clean HealthMonitor_custom.spec
```

---

## 📦 CO ZOSTANIE ZBUDOWANE?

Po zakończeniu procesu otrzymasz:

```
src/
├── dist/
│   └── HealthMonitor.exe    ← GOTOWY PLIK!
│
├── build/                    ← Pliki tymczasowe (można usunąć)
└── HealthMonitor_custom.spec ← Konfiguracja buildu
```

---

## ⚙️ DOSTOSOWANIE BUILDU

### Zmiana nazwy aplikacji

W pliku `build_exe.py`:

```python
'--name=HealthMonitor',  # Zmień na swoją nazwę
```

### Dodanie ikony

```python
'--icon=NONE',  # Zmień na: '--icon=ikona.ico'
```

### Build z konsolą debug

W pliku `build_exe.py`:

```python
'--windowed',  # Zmień na: '--console'
```

---

## 🎯 CECHY GOTOWEGO .EXE

✅ **Portable** - działa wszędzie bez instalacji
✅ **Standalone** - nie wymaga Pythona
✅ **Jeden plik** - wszystko w .exe
✅ **GUI** - bez okna konsoli
✅ **Kompletny** - wszystkie biblioteki dołączone

---

## 📊 WYMAGANIA DO BUDOWANIA

- Python 3.8+ zainstalowany
- Zależności z `requirements.txt` zainstalowane
- PyInstaller (auto-instalowany jeśli brak)
- ~500 MB wolnego miejsca

---

## 🆘 ROZWIĄZYWANIE PROBLEMÓW

### Build się nie udaje?

```bash
# Zainstaluj ponownie zależności
pip install --upgrade -r requirements.txt
pip install --upgrade pyinstaller

# Wyczyść cache
python -c "import shutil; shutil.rmtree('build', ignore_errors=True)"
python -c "import shutil; shutil.rmtree('dist', ignore_errors=True)"

# Spróbuj ponownie
python build_exe.py
```

### .exe nie uruchamia się?

- Sprawdź antywirus (może blokować)
- Dodaj do wyjątków antywirusa
- Uruchom jako administrator

---

## 📄 PLIKI PROJEKTU

- `BUILD_EXE.bat` - Automatyczny build (Windows)
- `build_exe.py` - Skrypt budowania
- `src/HealthMonitor_custom.spec` - Konfiguracja PyInstaller
- `BUILD_INSTRUCTIONS.md` - Pełna dokumentacja

---

**Status:** ✅ Gotowe do użycia!  
**Build date:** 13.01.2026  
**Wersja:** 1.0
