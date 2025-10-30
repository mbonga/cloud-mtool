# cloud-mtool

Small project — initial repository created via automation.

## Usage

Add project files and documentation.

## Demo

Run the demo CLI (no network calls are performed by default):

```zsh
PYTHONPATH=. python3 main.py
```

You can set config values from the CLI and dump current config:

```zsh
PYTHONPATH=. python3 main.py --set CMDB_URL=https://cmdb.example.com --dump-config
```

## Tests / CI

Unit tests use the standard library `unittest` and mock `requests` so they don't
perform network calls. To run locally:

```zsh
PYTHONPATH=. python3 -m unittest discover -v
```

There is a GitHub Actions workflow at `.github/workflows/ci.yml` which runs the
tests on push and pull requests.

