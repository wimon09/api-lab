# api-lab

API tests for the QuickPizza practice service, written with pytest and requests.

## Setup and run

Use Python 3.10 or newer:

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -v
```

The test suite sends requests to `https://quickpizza.grafana.com` and needs an
internet connection. Tests that create or change ratings use a newly created
test user and their own data. Do not use the public practice token to create or
change ratings.

To save the full run as a self-contained HTML report:

```sh
pytest -v --html=report.html --self-contained-html
```

## Input domain model: `POST /api/ratings`

Base choice uses 3 whole-number stars, an existing pizza, and the logged-in
user's token. Each non-base test changes one characteristic and leaves the
others at their base values.

| Characteristic | Blocks and example values | Covering tests |
|---|---|---|
| C1: value of stars | Below 1: `0`; base, 1 to 5: `3`; above 5: `6` | `test_stars_out_of_range[0]`, `test_base_choice_is_saved`, `test_stars_out_of_range[6]` |
| C2: type of stars | Base whole number: `3`; decimal: `3.5`; text: `"3"`; missing | `test_base_choice_is_saved`, `test_decimal_stars_are_refused`, `test_text_stars_are_refused`, `test_missing_stars_are_refused` |
| C3: pizza exists | Base existing pizza; does not exist: `999999999` | `test_base_choice_is_saved`, `test_pizza_does_not_exist` |
| C4: token | Base own token; no token; wrong-length token | `test_base_choice_is_saved`, `test_missing_token_is_refused`, `test_short_token_is_refused` |

This base choice model needs 9 tests: 1 base test plus 2 other C1 blocks, 3
other C2 blocks, 1 other C3 block, and 2 other C4 blocks. Testing every
combination would need `3 × 4 × 2 × 3 = 72` tests.