# CASE-001 — atomowy batch i duplikat

## Stan początkowy

Przypięta gałąź `case-001-broken`.

## Usterka

`ProjectRegistry.add_many` modyfikuje rejestr element po elemencie. Gdy duplikat pojawia się później w batchu, metoda zgłasza błąd, ale wcześniejsze elementy pozostają zapisane.

## Zadanie dla Executora

Napraw `ProjectRegistry.add_many`, aby walidacja całego batcha następowała przed mutacją stanu.

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
tests.test_registry.ProjectRegistryTests.test_duplicate_batch_does_not_partially_mutate_registry
```

## Warunek zaliczenia

- duplikat istniejący wcześniej zostaje odrzucony;
- duplikat wewnątrz batcha zostaje odrzucony;
- rejestr po błędzie jest identyczny jak przed wywołaniem;
- pełny zestaw testów przechodzi;
- diff jest ograniczony do najmniejszej potrzebnej zmiany.
