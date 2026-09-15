# Retail Discount Calculator

A portfolio refactor of an IS 2053 individual assignment on functions,
arguments, return values, conditionals, and user input.

## Behavior

- Accepts one or more item prices
- Applies a configurable discount when the subtotal reaches the threshold
- Uses `Decimal` so currency calculations do not rely on binary floating point
- Rejects empty transactions, negative prices, and invalid discount settings

## Run

```text
python main.py 25.00 40.00 50.00
```

Use `--threshold` or `--discount-rate` to explore other rules.

## Test

```text
python -m unittest -v test_main.py
```
