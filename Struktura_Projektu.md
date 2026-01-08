health_monitor/
    │─ .venv/                     # wirtualne środowisko (tworzone lokalnie)
	├─ .vscode/
	│   └─ settings.json          # ustawienia interpreterów VS Code
	├─ src/                       # kod źródłowy
        ├── main.py
    |   ├── health.kv
        ├── buildozer.spec
        ├── requirements.txt
    |   │
        ├── db/
        │   ├── __init__.py
    |   │   └── database.py
        │
        ├── models/
    |   │   ├── __init__.py
        │   └── measurements.py
        │
    |   ├── screens/
        │   ├── __init__.py
        │   ├── home.py
    |   │   ├── weight.py
        │   └── pressure.py
        │
    |   └── utils/
            ├── __init__.py
            └── validators.py
    ├─ tests/                     # testy jednostkowe
	│   └─ test_main.py
	├─ requirements.txt           # zależności Pythona
	└─ README.md                  # dokumentacja projektu
    |_ .gitignore                 # pliki wyłączone z kontroli wersji
    |_ .git                       # folder kontroli wersji