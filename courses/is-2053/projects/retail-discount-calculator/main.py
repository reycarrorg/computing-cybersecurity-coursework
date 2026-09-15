"""Calculate a retail transaction total with an optional discount.

Portfolio edition of an individual IS 2053 assignment.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from typing import Iterable, Sequence


CENTS = Decimal("0.01")


@dataclass(frozen=True)
class TransactionSummary:
    """An immutable, auditable summary of a transaction."""

    item_count: int
    subtotal: Decimal
    discount_rate: Decimal
    discount_amount: Decimal
    total: Decimal

    @property
    def discount_applied(self) -> bool:
        """Return whether the transaction received a discount."""

        return self.discount_amount > 0


def money(value: Decimal) -> Decimal:
    """Round a decimal value to the nearest cent."""

    return value.quantize(CENTS, rounding=ROUND_HALF_UP)


def calculate_transaction(
    prices: Iterable[Decimal],
    *,
    discount_threshold: Decimal = Decimal("100.00"),
    discount_rate: Decimal = Decimal("0.25"),
) -> TransactionSummary:
    """Return totals for a collection of nonnegative item prices."""

    items = tuple(prices)
    if not items:
        raise ValueError("at least one item price is required")
    if any(price < 0 for price in items):
        raise ValueError("item prices cannot be negative")
    if discount_threshold < 0:
        raise ValueError("discount threshold cannot be negative")
    if not Decimal("0") <= discount_rate <= Decimal("1"):
        raise ValueError("discount rate must be between 0 and 1")

    subtotal = money(sum(items, start=Decimal("0")))
    applied_rate = discount_rate if subtotal >= discount_threshold else Decimal("0")
    discount_amount = money(subtotal * applied_rate)
    total = money(subtotal - discount_amount)

    return TransactionSummary(
        item_count=len(items),
        subtotal=subtotal,
        discount_rate=applied_rate,
        discount_amount=discount_amount,
        total=total,
    )


def decimal_argument(raw_value: str) -> Decimal:
    """Parse a command-line decimal and return a useful validation error."""

    try:
        return Decimal(raw_value)
    except InvalidOperation as exc:
        raise argparse.ArgumentTypeError(f"invalid decimal value: {raw_value}") from exc


def build_parser() -> argparse.ArgumentParser:
    """Create the command-line parser."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("prices", nargs="+", type=decimal_argument, help="item prices")
    parser.add_argument(
        "--threshold",
        type=decimal_argument,
        default=Decimal("100.00"),
        help="subtotal required for a discount (default: 100.00)",
    )
    parser.add_argument(
        "--discount-rate",
        type=decimal_argument,
        default=Decimal("0.25"),
        help="discount as a decimal fraction (default: 0.25)",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the command-line application."""

    args = build_parser().parse_args(argv)
    try:
        summary = calculate_transaction(
            args.prices,
            discount_threshold=args.threshold,
            discount_rate=args.discount_rate,
        )
    except ValueError as exc:
        print(f"Error: {exc}")
        return 2

    print(f"Items: {summary.item_count}")
    print(f"Subtotal: ${summary.subtotal:.2f}")
    if summary.discount_applied:
        print(f"Discount ({summary.discount_rate:.0%}): -${summary.discount_amount:.2f}")
    else:
        print("Discount: not applied")
    print(f"Total: ${summary.total:.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
