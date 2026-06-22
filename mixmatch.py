"""NOD Mix & Match v2 — negotiation tool randomizer (CLI).

Usage:
    python mixmatch.py --duration 10

Set per-tool counts with --counts or edit TOOLS below.
"""
from __future__ import annotations

import argparse
import random
import sys
import time
from dataclasses import dataclass, field


@dataclass
class Tool:
    name: str
    description: str
    count: int = 1


TOOLS = [
    Tool("Mirror", "Repeat last 1 to 3 words of the core concept."),
    Tool("Label", '"It seems like ..." "It sounds like ..." "It looks like ..." "It feels like ..."'),
    Tool("Clean Language", "What kind of X is that X? Is anything else about that X?"),
    Tool("Summary", 'Trigger a "that\'s right." — label + paraphrase, affirm "the world according to ..."'),
    Tool("Calibrated Questions", "What, How, sometimes reverse Why. Eg: How does this fit? What makes you ask?"),
    Tool("Loss Aversion", "Pain of losing is 2× the pleasure of gaining. Losses drive stronger emotional responses."),
    Tool("Dynamic Silence", "Plan 3+ seconds of silence. Counterpart usually breaks in ~7. Use any tool afterward.", 3),
    Tool("Paraphrase", "Express the meaning using different words for greater clarity."),
    Tool("Miss Label", "Label something incorrectly or falsely."),
    Tool("Trigger", "Cause fear, shock, anger, or worry — especially by reminding of past bad events."),
    Tool("No Oriented Question", 'Have you given up on ...? Is it ridiculous ...? Would it be horrible ...? Is it a bad idea ...?'),
    Tool("Accusation Audit", 'Call it out instead of denying: "It probably seems like ..."'),
]


def build_deck(tools: list[Tool]) -> list[Tool]:
    deck = [t for t in tools for _ in range(t.count)]
    random.shuffle(deck)
    return deck


def fmt_time(seconds: int) -> str:
    m, s = divmod(seconds, 60)
    return f"{m:02d}:{s:02d}"


def run_session(duration_minutes: int):
    deck = build_deck(TOOLS)
    end = time.time() + duration_minutes * 60
    history: list[str] = []

    print(f"\n  NOD Mix & Match  —  {duration_minutes} min session\n")

    while time.time() < end and deck:
        remaining = int(end - time.time())
        print(f"  [{fmt_time(remaining)}]  Hit Enter for next tool, Ctrl+C to quit.", end="", flush=True)
        try:
            input()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        t = deck.pop()
        history.append(t.name)
        # clear the prompt line
        print(f"\r\x1b[K  \033[36m{t.name}\033[0m")
        print(f"     {t.description}\n")

    if not deck and time.time() < end:
        print(f"  [{fmt_time(int(end - time.time()))}]  Deck exhausted — reshuffling.")
        deck = build_deck(TOOLS)
        # Keep going without recursion
        while time.time() < end and deck:
            remaining = int(end - time.time())
            print(f"  [{fmt_time(remaining)}]  Hit Enter for next tool, Ctrl+C to quit.", end="", flush=True)
            try:
                input()
            except (EOFError, KeyboardInterrupt):
                print()
                break
            t = deck.pop()
            history.append(t.name)
            print(f"\r\x1b[K  \033[36m{t.name}\033[0m")
            print(f"     {t.description}\n")

    print(f"\n  \033[33mSession done.\033[0m  Used {len(history)} tools.")
    if history:
        print(f"  History: {', '.join(history)}")
    print()


def main():
    p = argparse.ArgumentParser(description="NOD Mix & Match v2 — negotiation tool randomizer")
    p.add_argument("--duration", "-d", type=int, default=10, help="Session length in minutes (default: 10)")
    args = p.parse_args()
    try:
        run_session(args.duration)
    except KeyboardInterrupt:
        print("\n  Stopped.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())