"""Store, display, and summarize golf tournament scores.

Portfolio edition of an individual IS 2053 assignment.
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path
from statistics import mean
from typing import Iterable, Sequence


@dataclass(frozen=True)
class GolfScore:
    """A validated player name and score."""

    player: str
    score: int

    def __post_init__(self) -> None:
        normalized_name = self.player.strip()
        if not normalized_name:
            raise ValueError("player name cannot be empty")
        if not 0 <= self.score <= 300:
            raise ValueError("score must be between 0 and 300")
        object.__setattr__(self, "player", normalized_name)


@dataclass(frozen=True)
class TournamentSummary:
    """Summary statistics for a set of golf scores."""

    player_count: int
    lowest_score: int
    highest_score: int
    average_score: float


def write_scores(path: Path, scores: Iterable[GolfScore], *, append: bool = False) -> None:
    """Write validated scores to a CSV file."""

    mode = "a" if append else "w"
    path.parent.mkdir(parents=True, exist_ok=True)
    needs_header = not append or not path.exists() or path.stat().st_size == 0
    with path.open(mode, newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=["player", "score"])
        if needs_header:
            writer.writeheader()
        for entry in scores:
            writer.writerow({"player": entry.player, "score": entry.score})


def read_scores(path: Path) -> list[GolfScore]:
    """Read scores from CSV and reject malformed rows."""

    if not path.exists():
        raise FileNotFoundError(f"score file not found: {path}")

    entries: list[GolfScore] = []
    with path.open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != ["player", "score"]:
            raise ValueError("score file must contain player and score columns")
        for row_number, row in enumerate(reader, start=2):
            try:
                entries.append(GolfScore(row["player"], int(row["score"])))
            except (TypeError, ValueError) as exc:
                raise ValueError(f"invalid score data on row {row_number}") from exc
    return entries


def summarize_scores(scores: Iterable[GolfScore]) -> TournamentSummary:
    """Calculate summary statistics for one or more scores."""

    entries = tuple(scores)
    if not entries:
        raise ValueError("at least one score is required")
    values = [entry.score for entry in entries]
    return TournamentSummary(
        player_count=len(entries),
        lowest_score=min(values),
        highest_score=max(values),
        average_score=mean(values),
    )


def build_parser() -> argparse.ArgumentParser:
    """Create the command-line parser."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--file", type=Path, default=Path("golf-scores.csv"))
    commands = parser.add_subparsers(dest="command", required=True)

    add_parser = commands.add_parser("add", help="append a player's score")
    add_parser.add_argument("player")
    add_parser.add_argument("score", type=int)
    commands.add_parser("list", help="display all scores")
    commands.add_parser("summary", help="display tournament statistics")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the command-line application."""

    args = build_parser().parse_args(argv)
    try:
        if args.command == "add":
            entry = GolfScore(args.player, args.score)
            write_scores(args.file, [entry], append=True)
            print(f"Saved {entry.player}: {entry.score}")
            return 0

        entries = read_scores(args.file)
        if args.command == "list":
            for entry in entries:
                print(f"{entry.player}: {entry.score}")
            return 0

        summary = summarize_scores(entries)
        print(f"Players: {summary.player_count}")
        print(f"Lowest score: {summary.lowest_score}")
        print(f"Highest score: {summary.highest_score}")
        print(f"Average score: {summary.average_score:.2f}")
        return 0
    except (FileNotFoundError, ValueError) as exc:
        print(f"Error: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
