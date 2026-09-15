"""Tests for the golf score tracker."""

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from golf_scores import GolfScore, read_scores, summarize_scores, write_scores


class GolfScoreTrackerTests(unittest.TestCase):
    def test_round_trip_csv(self) -> None:
        scores = [GolfScore("Alex", 82), GolfScore("Jordan", 77)]
        with TemporaryDirectory() as directory:
            path = Path(directory) / "scores.csv"
            write_scores(path, scores)

            self.assertEqual(read_scores(path), scores)

    def test_append_preserves_existing_scores(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "scores.csv"
            write_scores(path, [GolfScore("Alex", 82)])
            write_scores(path, [GolfScore("Jordan", 77)], append=True)

            self.assertEqual(len(read_scores(path)), 2)

    def test_summary(self) -> None:
        summary = summarize_scores(
            [GolfScore("Alex", 82), GolfScore("Jordan", 77), GolfScore("Sam", 91)]
        )

        self.assertEqual(summary.player_count, 3)
        self.assertEqual(summary.lowest_score, 77)
        self.assertEqual(summary.highest_score, 91)
        self.assertAlmostEqual(summary.average_score, 83.3333333333)

    def test_rejects_invalid_score(self) -> None:
        with self.assertRaisesRegex(ValueError, "between 0 and 300"):
            GolfScore("Alex", 301)

    def test_rejects_empty_name(self) -> None:
        with self.assertRaisesRegex(ValueError, "cannot be empty"):
            GolfScore("  ", 82)


if __name__ == "__main__":
    unittest.main()
