# Contributing to Health Monitor

Dziękujemy za zainteresowanie współpracą przy projekcie Health Monitor! 🎉

## Jak mogę pomóc?

### Zgłaszanie błędów

- Sprawdź czy błąd nie został już zgłoszony
- Stwórz nowy Issue z dokładnym opisem
- Dołącz kroki do reprodukcji
- Dodaj zrzuty ekranu jeśli to możliwe

### Proponowanie nowych funkcjonalności

- Otwórz Issue z etykietą "enhancement"
- Opisz szczegółowo proponowaną funkcjonalność
- Wyjaśnij dlaczego byłaby przydatna

### Pull Requests

1. **Fork repozytorium**
2. **Stwórz branch z opisową nazwą:**

   ```bash
   git checkout -b feature/nazwa-funkcjonalności
   git checkout -b fix/nazwa-poprawki
   ```

3. **Wprowadź zmiany:**

   - Pisz czytelny kod zgodny z PEP 8
   - Dodaj docstringi do funkcji i klas
   - Stwórz testy dla nowych funkcjonalności
   - Upewnij się że wszystkie testy przechodzą

4. **Commit zmian:**

   ```bash
   git commit -m "Dodano: krótki opis zmian"
   ```

5. **Push do swojego forka:**

   ```bash
   git push origin feature/nazwa-funkcjonalności
   ```

6. **Otwórz Pull Request**

## Standardy Kodu

### Python

- Zgodność z PEP 8
- Używaj type hints gdzie to możliwe
- Docstringi dla wszystkich funkcji publicznych
- Maksymalna długość linii: 88 znaków (Black formatter)

### Testy

- Każda nowa funkcjonalność powinna mieć testy
- Testy powinny pokrywać różne scenariusze (happy path, edge cases)
- Używaj znaczących nazw testów

### Commity

Używaj konwencji Conventional Commits:

- `feat:` - nowa funkcjonalność
- `fix:` - poprawka błędu
- `docs:` - zmiany w dokumentacji
- `test:` - dodanie lub modyfikacja testów
- `refactor:` - refaktoryzacja kodu

Przykłady:

```
feat: dodano eksport danych do PDF
fix: poprawiono błąd w obliczaniu średniej glukozy
docs: zaktualizowano README
test: dodano testy dla modułu użytkowników
```

## Proces Review

1. Maintainer sprawdzi Twój Pull Request
2. Mogą być sugestie zmian
3. Po akceptacji kod zostanie zmergowany do main

## Pytania?

Jeśli masz pytania, śmiało otwórz Issue lub skontaktuj się przez Discussions.

Dziękujemy za pomoc w rozwoju Health Monitor! ❤️
