# Golf Score Tracker

A portfolio refactor of an IS 2053 individual file-handling assignment. The
original program saved and displayed player scores; this edition adds reusable
functions, CSV validation, a command-line interface, summary statistics, and
tests.

## Run

```text
python golf_scores.py --file golf-scores.csv add "Alex Morgan" 82
python golf_scores.py --file golf-scores.csv list
python golf_scores.py --file golf-scores.csv summary
```

## Test

```text
python -m unittest -v test_golf_scores.py
```
