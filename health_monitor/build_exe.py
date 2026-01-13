"""
Skrypt do budowania aplikacji Health Monitor jako standalone .exe
Używa PyInstaller do stworzenia przenośnej wersji aplikacji
"""

import os
import sys
import shutil
import subprocess


def clean_build_dirs():
    """Czyści poprzednie pliki build i dist"""
    dirs_to_clean = ["build", "dist", "__pycache__"]
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"Czyszczę katalog: {dir_name}")
            shutil.rmtree(dir_name)

    # Usuń spec file jeśli istnieje
    spec_file = "HealthMonitor.spec"
    if os.path.exists(spec_file):
        print(f"Usuwam poprzedni plik spec: {spec_file}")
        os.remove(spec_file)


def check_pyinstaller():
    """Sprawdza czy PyInstaller jest zainstalowany"""
    try:
        import PyInstaller

        print(f"✓ PyInstaller zainstalowany: wersja {PyInstaller.__version__}")
        return True
    except ImportError:
        print("✗ PyInstaller nie jest zainstalowany")
        print("\nInstaluję PyInstaller...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
        return True


def build_exe():
    """Buduje plik .exe"""

    print("\n" + "=" * 60)
    print("  BUDOWANIE HEALTH MONITOR - PORTABLE EXE")
    print("=" * 60 + "\n")

    # Sprawdź PyInstaller
    if not check_pyinstaller():
        return False

    # Wyczyść poprzednie buildy
    clean_build_dirs()

    # Przejdź do katalogu src
    os.chdir("src")

    # Parametry PyInstaller
    pyinstaller_args = [
        "main.py",
        "--name=HealthMonitor",
        "--onefile",  # Jeden plik .exe
        "--windowed",  # Bez konsoli (GUI app)
        "--icon=NONE",  # Możesz dodać własną ikonę: --icon=icon.ico
        "--noconfirm",  # Nie pytaj o nadpisanie
        # Dołącz wszystkie potrzebne pliki
        "--add-data=health.kv;.",
        # Ukryte importy dla Kivy - podstawowe moduły
        "--hidden-import=kivy.core.window.window_info",
        "--hidden-import=kivy.core.text",
        "--hidden-import=kivy.core.image",
        "--hidden-import=kivy.input.providers.mouse",
        "--hidden-import=win32timezone",
        # Matplotlib
        "--hidden-import=matplotlib.pyplot",
        "--hidden-import=matplotlib.backends.backend_agg",
        # ReportLab
        "--hidden-import=reportlab.pdfgen.canvas",
        "--hidden-import=reportlab.lib.pagesizes",
        "--hidden-import=reportlab.pdfbase",
        "--hidden-import=reportlab.pdfbase.ttfonts",
        # Garden graph
        "--hidden-import=kivy_garden.graph",
        "--hidden-import=kivy_garden.graph.graph",
        # Dodatkowe wymagane moduły
        "--hidden-import=pkg_resources.extern",
        # Kolekcje danych - uproszczone
        "--collect-data=kivy_deps.sdl2",
        "--collect-data=kivy_deps.glew",
        "--collect-data=kivy_deps.angle",
        "--collect-binaries=kivy_deps.sdl2",
        "--collect-binaries=kivy_deps.glew",
        "--collect-binaries=kivy_deps.angle",
        # Debugowanie (opcjonalne - usuń dla finalnej wersji)
        # '--debug=all',
    ]

    print("\nUruchamianie PyInstaller...")
    print(f"Komenda: pyinstaller {' '.join(pyinstaller_args)}\n")

    # Uruchom PyInstaller
    result = subprocess.run(["pyinstaller"] + pyinstaller_args)

    # Wróć do głównego katalogu
    os.chdir("..")

    if result.returncode == 0:
        print("\n" + "=" * 60)
        print("  ✓ SUKCES! Aplikacja została zbudowana")
        print("=" * 60)
        print(f"\nPlik .exe znajduje się w: src/dist/HealthMonitor.exe")
        print("\nInformacje o aplikacji portable:")
        print("- Możesz skopiować plik .exe w dowolne miejsce")
        print("- Baza danych zostanie utworzona w katalogu z .exe")
        print("- Wszystkie backupy i eksporty również w tym katalogu")
        print("\nAby przetestować:")
        print("1. Skopiuj src/dist/HealthMonitor.exe w wybrane miejsce")
        print("2. Uruchom aplikację")
        print("3. Dane będą zapisywane lokalnie obok .exe")
        return True
    else:
        print("\n" + "=" * 60)
        print("  ✗ BŁĄD podczas budowania")
        print("=" * 60)
        return False


if __name__ == "__main__":
    try:
        success = build_exe()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ Wystąpił błąd: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
