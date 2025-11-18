# -*- coding: utf-8 -*-
"""
deck_normalizer.py

Nimmt das Roh-Deck aus content_raw_parser.py (deck_semantic.json)
und bringt es in eine Struktur, die vom layout_planner_agent.py verstanden wird:

- Kopiert meta
- Erzeugt pro Slide:
  - id
  - intent
  - semantic_role (derzeit einfach = intent)
  - analysis (aus derived_features)
  - segments: Liste von {type, text}
"""

import json
import argparse
from typing import Any, Dict, List


def normalize_slide(slide: Dict[str, Any]) -> Dict[str, Any]:
    """Mappt die flachen Felder (title, body_text, bullets)
    in eine einfache Segment-Struktur + analysis."""
    segments: List[Dict[str, str]] = []

    title = (slide.get("title") or "").strip()
    if title:
        segments.append({"type": "title", "text": title})

    # body_text → ein Segment (später kann man das feiner splitten)
    body_text = (slide.get("body_text") or "").strip()
    if body_text:
        segments.append({"type": "text", "text": body_text})

    # bullets → je Bullet ein Segment (type = "bullet")
    bullets = slide.get("bullets") or []
    for b in bullets:
        b_txt = (b or "").strip()
        if b_txt:
            segments.append({"type": "bullet", "text": b_txt})

    return {
        "id": slide.get("id"),
        "intent": slide.get("intent"),
        # fürs erste: semantic_role = intent (kann später feiner klassifiziert werden)
        "semantic_role": slide.get("intent"),
        # layout_planner_agent erwartet "analysis", daher hier Mapping
        "analysis": slide.get("derived_features") or {},
        "segments": segments,
    }


def normalize_deck(deck: Dict[str, Any]) -> Dict[str, Any]:
    slides_in = deck.get("slides", []) or []
    slides_out = [normalize_slide(s) for s in slides_in]
    return {
        "meta": deck.get("meta", {}),
        "slides": slides_out,
    }


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Normalisiert deck_semantic.json für layout_planner_agent.py"
    )
    ap.add_argument("--in", dest="inp", required=True,
                    help="Input-Deck (z. B. out/deck_semantic.json)")
    ap.add_argument("--out", dest="out", required=True,
                    help="Output-Deck (z. B. out/deck_semantic_norm.json)")
    args = ap.parse_args()

    with open(args.inp, "r", encoding="utf-8") as f:
        deck = json.load(f)

    norm = normalize_deck(deck)

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(norm, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
