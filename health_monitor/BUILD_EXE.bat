@echo off
chcp 65001 >nul
echo ============================================================
echo   BUDOWANIE HEALTH MONITOR - PORTABLE .EXE
echo ============================================================
echo.

REM Aktywuj środowisko wirtualne jeśli istnieje
if exist ".venv\Scripts\activate.bat" (
    echo Aktywuję środowisko wirtualne...
    call .venv\Scripts\activate.bat
) else (
    echo Używam systemowego Python...
)

echo.
echo Uruchamiam skrypt budowania...
echo.

python build_exe.py

echo.
echo ============================================================
echo   Proces zakończony
echo ============================================================
echo.
pause
