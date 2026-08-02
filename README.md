# Executor Pilot Target

Kontrolowane repozytorium szkoleniowo-testowe dla projektu `litrgratis-pixel/Executor`.

Repo służy wyłącznie do sprawdzenia pionowego przepływu Executora na małym, deterministycznym projekcie Python. Nie jest produktem, platformą ani dowodem wartości biznesowej Executora.

## Zakres

Projekt udostępnia prosty rejestr projektów z trzema zachowaniami używanymi jako przypadki pilota:

1. atomowe dodawanie batcha bez częściowego zapisu po wykryciu duplikatu;
2. blokowanie `CLOSED -> ACTIVE` bez przyczyny wznowienia;
3. kanoniczny, deterministyczny JSON niezależny od kolejności wejścia.

Pełne granice zawiera [`PILOT_CONTRACT.md`](PILOT_CONTRACT.md). Opisy przypadków znajdują się w katalogu [`cases/`](cases/).

## Uruchomienie

```bash
python -m compileall -q project_registry tests
python -m unittest discover -s tests -v
python -m project_registry.cli canonicalize examples/projects.json
```

Projekt wymaga Python `>=3.11` i nie ma zależności uruchomieniowych.

## Model gałęzi

- `main` — zaakceptowana poprawna baza referencyjna;
- `case-001-broken` — kontrolowana regresja atomowości batcha;
- `case-002-broken` — kontrolowana regresja autoryzacji wznowienia;
- `case-003-broken` — kontrolowana regresja deterministycznego wyjścia;
- gałęzie naprawcze — tworzone przez Executor od konkretnej gałęzi `case-*`.

Gałąź `case-*` nie jest nieudanym stanem produktu. Jest niezmiennym wejściem benchmarku. Nie wolno jej naprawiać bezpośrednio ani scalać do `main`.

## Granica dowodu

Zaliczenie przypadków w tym repo może potwierdzić działanie mechanizmu wykonawczego, polityki zmian, sandboxa, testów i raportowania. Nie potwierdza, że Executor rozwiązuje wartościowy problem użytkownika. Taki dowód musi pochodzić z późniejszego pilota w rzeczywistym repozytorium.
