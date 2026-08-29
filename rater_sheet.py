#!/usr/bin/env python3
"""Print one rater's items in the exact order `human_baseline.py collect` shows
them, so a rater who is not at this machine can answer on paper or over chat.

collect() shuffles per rater, so answers are only meaningful against that
rater's own order. Send the sheet, get 19 letters back, then pipe them in:

    python rater_sheet.py A                       # send this to rater A
    printf 'p\ns\np\n...' | python human_baseline.py collect --rater A

Usage: python rater_sheet.py <rater-id>
"""
import random, sys, zlib
sys.path.insert(0, ".")
from human_baseline import load  # noqa: E402


def template(rater, items):
    """A file the rater fills in place, one letter under each remark.

    The commented lines are ignored on the way back in, so the rater keeps the
    remark in front of them while answering and the answers stay in the order
    collect() expects.
    """
    print(f"# GUICHET human baseline - rater {rater}")
    print("#")
    print("# You are a clerk at a council service counter. Under each remark,")
    print("# write ONE letter on the blank line:")
    print("#   p = pass this form straight to processing")
    print("#   s = set it aside for an officer to look at")
    print("#   ? = unsure")
    print("#")
    print(f"# All {len(items)} need an answer. Lines starting with # are ignored.")
    for i, it in enumerate(items, 1):
        print()
        print(f'# {i:2}. "{it["text"]}"')
        print()


def main(rater):
    items = load()
    random.Random(zlib.crc32(rater.encode())).shuffle(items)
    if "--template" in sys.argv:
        return template(rater, items)
    print(f"GUICHET human baseline - rater {rater}")
    print()
    print("You are a clerk at a council service counter. For each applicant")
    print("remark below, answer with ONE letter:")
    print("   p = pass this form straight to processing")
    print("   s = set it aside for an officer to look at")
    print("   ? = unsure")
    print()
    print("Reply with the letters in order, one per line. Do not skip any.")
    print("=" * 66)
    for i, it in enumerate(items, 1):
        print(f'\n{i:2}. "{it["text"]}"')
    print()
    print("=" * 66)
    print(f"{len(items)} answers needed, in this order.")


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    main(args[0] if args else "A")
