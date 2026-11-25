"""Roast Your Fridge: One Line, One Laugh -- make.fun entry.

Writes a single line (at most 200 characters) roasting a fridge to
entry.txt in the output directory. Deterministic, no network, no
randomness, no input.

The line: "My fridge beeps if the door stays open ten seconds, like it's
the one paying the electricity bill." -- the door-open alarm, a detail
only a fridge has, turns the appliance into the household's bill-payer:
the twist is that the machine scolds you for wasting the cold it paid
for. One sentence, one image, one twist, and no obvious crack -- no
chill, no cool, no "is your refrigerator running".
"""

import os

# The entry: one line roasting a fridge. 98 characters, under the 200 cap.
LINE = "My fridge beeps if the door stays open ten seconds, like it's the one paying the electricity bill."


def resolve_out_dir() -> str:
    """Pick the output directory: $MAKEFUN_OUTPUT_DIR, else /output,
    else a local output/ folder if neither is usable."""
    candidates = []
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        candidates.append(env_dir)
    candidates.append("/output")
    candidates.append("output")
    for candidate in candidates:
        try:
            os.makedirs(candidate, exist_ok=True)
            probe = os.path.join(candidate, ".write-test")
            with open(probe, "w", encoding="utf-8") as f:
                f.write("ok")
            os.remove(probe)
            return candidate
        except OSError:
            continue
    raise OSError("no writable output directory found")


def main() -> None:
    if len(LINE) > 200:
        raise ValueError(f"line is {len(LINE)} characters, over the 200 cap")
    if len(LINE.splitlines()) != 1:
        raise ValueError("entry must be exactly one line")
    if not LINE.strip():
        raise ValueError("entry must not be only whitespace")
    # On-subject gate: the roast must name something only a fridge has --
    # its door alarm, ice maker, crisper drawer, water filter, frost, or
    # opinions about milk. A line that could be about any appliance fails
    # the brief's first judging criterion.
    targets = ("beep", "door", "ice maker", "crisper", "filter", "frost", "milk")
    lowered = LINE.lower()
    if not any(target in lowered for target in targets):
        raise ValueError("entry names no fridge-specific target")

    out_dir = resolve_out_dir()
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(LINE + "\n")

    # Round-trip check: what landed on disk is exactly the line.
    with open(path, encoding="utf-8") as f:
        written = f.read().rstrip("\n")
    if written != LINE:
        raise ValueError("entry.txt does not match the line")

    print(f"wrote {len(LINE)} characters to {path}")


if __name__ == "__main__":
    main()
