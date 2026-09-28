#!/usr/bin/env python3
"""Convert a SHAGGY26K mania=5 chart into the custom mania=9 100K-opponent/4K-BF layout.

Usage:
    python convert_26k_to_100x4.py input.json output.json

The converter keeps timing, sustain lengths, note types, sections, BPM and characters.
Enemy notes are spread deterministically across the 100 lanes; BF notes are folded to 4K.
"""

import json
import sys
from pathlib import Path

OLD_KEYS = 26
ENEMY_KEYS = 100
PLAYER_KEYS = 4
NEW_MANIA = 9


def enemy_lane_26_to_100(old_lane: int, counters: list[int]) -> int:
    """Spread repeated notes from one old lane across its proportional 100K bucket."""
    start = (old_lane * ENEMY_KEYS) // OLD_KEYS
    end = ((old_lane + 1) * ENEMY_KEYS) // OLD_KEYS
    width = max(1, end - start)
    lane = start + (counters[old_lane] % width)
    counters[old_lane] += 1
    return min(ENEMY_KEYS - 1, lane)


def convert_chart(data: dict) -> dict:
    song = data.get("song", data)
    if not isinstance(song, dict):
        raise ValueError("JSON inválido: no se encontró el objeto 'song'.")

    old_mania = int(song.get("mania", 5))
    if old_mania != 5:
        print(f"Aviso: el chart tiene mania={old_mania}; se convertirá igualmente suponiendo formato 26K.")

    counters = [0] * OLD_KEYS

    for section in song.get("notes", []):
        must_hit = bool(section.get("mustHitSection", False))
        converted_notes = []

        for note in section.get("sectionNotes", []):
            if not isinstance(note, list) or len(note) < 2:
                converted_notes.append(note)
                continue

            raw = int(note[1])
            if raw < 0:  # Event note; leave untouched.
                converted_notes.append(note)
                continue

            old_lane = raw % OLD_KEYS
            in_primary_half = raw < OLD_KEYS
            is_player = must_hit if in_primary_half else not must_hit

            if is_player:
                new_lane = old_lane % PLAYER_KEYS
                # Mixed layout: when BF owns section, BF is 0..3; otherwise BF is 100..103.
                new_raw = new_lane if must_hit else ENEMY_KEYS + new_lane
            else:
                new_lane = enemy_lane_26_to_100(old_lane, counters)
                # Mixed layout: when enemy owns section, enemy is 0..99; otherwise 4..103.
                new_raw = new_lane if not must_hit else PLAYER_KEYS + new_lane

            new_note = list(note)
            new_note[1] = new_raw
            converted_notes.append(new_note)

        section["sectionNotes"] = converted_notes

    song["mania"] = NEW_MANIA
    return data


def main() -> int:
    if len(sys.argv) != 3:
        print("Uso: python convert_26k_to_100x4.py input.json output.json")
        return 2

    src = Path(sys.argv[1])
    dst = Path(sys.argv[2])

    with src.open("r", encoding="utf-8") as f:
        data = json.load(f)

    data = convert_chart(data)

    dst.parent.mkdir(parents=True, exist_ok=True)
    with dst.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))

    print(f"Convertido: {src} -> {dst}")
    print("Nuevo modo: mania=9 | enemigo=100K | BF=4K")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
