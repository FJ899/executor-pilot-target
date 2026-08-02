# CASE-002 — wznowienie zamkniętego projektu

## Stan początkowy

Przypięta gałąź `case-002-broken`.

## Usterka

`ProjectRegistry.transition` pozwala przejść z `CLOSED` do `ACTIVE` bez podania przyczyny wznowienia.

## Zadanie dla Executora

Przywróć regułę wymagającą niepustego `reopen_reason` dla przejścia `CLOSED -> ACTIVE`.

## Dozwolony zakres

```text
project_registry/registry.py
```

## Zakazany zakres

- testy;
- kontrakt pilota;
- pozostałe moduły;
- workflow CI;
- konfiguracja projektu.

## Test ujawniający problem

```text
tests.test_registry.ProjectRegistryTests.test_closed_project_requires_reason_before_reopening
```

## Warunek zaliczenia

- `ACTIVE -> CLOSED` nadal działa;
- `CLOSED -> ACTIVE` bez przyczyny jest blokowane;
- stan po odrzuconej zmianie pozostaje `CLOSED`;
- `CLOSED -> ACTIVE` z przyczyną działa i zapisuje oczyszczony tekst;
- pełny zestaw testów przechodzi;
- diff nie rozszerza modelu stanów.
