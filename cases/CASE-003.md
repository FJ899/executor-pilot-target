# CASE-003 — deterministyczny wynik JSON

## Stan początkowy

Przypięta gałąź `case-003-broken`.

## Usterka

`ProjectRegistry.to_payload` zachowuje kolejność dodania projektów. Ten sam zbiór danych daje różne bajty wyjściowe zależnie od kolejności wejścia.

## Zadanie dla Executora

Przywróć kanoniczną kolejność projektów według `project_id` bez utraty znaków UTF-8.

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

## Testy ujawniające problem

```text
tests.test_registry.ProjectRegistryTests.test_json_output_is_sorted_stable_and_utf8_friendly
tests.test_cli.ProjectRegistryCliTests.test_different_input_order_produces_identical_stdout
```

## Warunek zaliczenia

- różna kolejność wejścia daje identyczny wynik;
- projekty są posortowane po `project_id`;
- znaki takie jak `Ł` i `Ż` nie są zamieniane na sekwencje ASCII;
- wynik kończy się jednym znakiem nowej linii;
- plik wejściowy nie jest modyfikowany;
- pełny zestaw testów przechodzi.
