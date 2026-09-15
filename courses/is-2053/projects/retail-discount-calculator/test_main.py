"""Tests for the retail discount calculator."""

from decimal import Decimal
import unittest

from main import calculate_transaction


class CalculateTransactionTests(unittest.TestCase):
    def test_applies_discount_at_threshold(self) -> None:
        summary = calculate_transaction(
            [Decimal("25.00"), Decimal("35.00"), Decimal("40.00")]
        )

        self.assertEqual(summary.subtotal, Decimal("100.00"))
        self.assertEqual(summary.discount_amount, Decimal("25.00"))
        self.assertEqual(summary.total, Decimal("75.00"))
        self.assertTrue(summary.discount_applied)

    def test_does_not_apply_discount_below_threshold(self) -> None:
        summary = calculate_transaction([Decimal("12.50"), Decimal("7.25")])

        self.assertEqual(summary.subtotal, Decimal("19.75"))
        self.assertEqual(summary.discount_amount, Decimal("0.00"))
        self.assertEqual(summary.total, Decimal("19.75"))

    def test_rounds_currency_to_cents(self) -> None:
        summary = calculate_transaction(
            [Decimal("100.01")], discount_rate=Decimal("0.10")
        )

        self.assertEqual(summary.discount_amount, Decimal("10.00"))
        self.assertEqual(summary.total, Decimal("90.01"))

    def test_rejects_negative_price(self) -> None:
        with self.assertRaisesRegex(ValueError, "negative"):
            calculate_transaction([Decimal("-1.00")])

    def test_rejects_empty_transaction(self) -> None:
        with self.assertRaisesRegex(ValueError, "at least one"):
            calculate_transaction([])


if __name__ == "__main__":
    unittest.main()
