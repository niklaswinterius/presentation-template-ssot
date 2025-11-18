# -*- coding: utf-8 -*-
"""
content_raw_parser.py
Parst content_raw.md und erzeugt deck_semantic.json für die Layoutentscheidung.
CLI:
  python content_raw_parser.py --in content\content_raw.md --out deck_semantic.json
"""
import re, json, argparse
from typing import List, Dict, Any

REL_MAP = {
    "comparison": [" vs. ", "gegenüberstellung", "vergleich"],
    "before_after": ["heute", "zielbild", "before", "after", "vorher", "nachher"],
    "problem_solution": ["problem", "lösung"],
    "pros_cons": ["vor-/nachteile", "pros", "cons"]
}

def guess_relation_type(text: str) -> str:
    t = text.lower()
    scores = {rel: sum(1 for kw in kws if kw in t) for rel, kws in REL_MAP.items()}
    best = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)
    return best[0][0] if best and best[0][1] > 0 else "single_story"

def split_slides(md: str) -> List[Dict[str, Any]]:
    blocks = re.split(r"\n(?=###\s+)", md)
    out: List[Dict[str, Any]] = []
    for b in blocks:
        m = re.match(r"###\s+(.+)\n(.*)", b.strip(), re.DOTALL)
        if not m: 
            continue
        title = m.group(1).strip()
        body = (m.group(2) or "").strip()
        bullets = [re.sub(r"^\s*-\s*", "", ln).strip() for ln in body.splitlines() if re.match(r"^\s*-\s+", ln)]
        paragraphs = [ln.strip() for ln in body.split("\n") if ln.strip() and not ln.strip().startswith("-")]
        body_text = "\n".join(paragraphs).strip()
        explicit = re.search(r"\[relation:\s*(\w+)\s*\]", body.lower())
        rel = explicit.group(1) if explicit else guess_relation_type(title + " " + body)
        if rel == "single_story":
            segs, rel_norm = 1, "overview"
        elif rel in ("comparison","before_after","problem_solution","pros_cons"):
            segs, rel_norm = 2, rel
        else:
            segs, rel_norm = 1, "overview"
        dom = "bullets" if len(bullets) >= 3 else ("text" if body_text else "bullets" if bullets else "text")
        total_chars = sum(len(b) for b in bullets) + len(body_text)
        intent = "comparison" if segs == 2 else ("bullet" if bullets else "bullet")
        out.append({
            "id": f"S{len(out)+1:02d}",
            "intent": intent,
            "title": title,
            "bullets": bullets or None,
            "body_text": body_text or None,
            "derived_features": {
                "segment_count": segs,
                "relation_type": rel_norm,
                "dominant_type": dom,
                "total_chars": total_chars
            }
        })
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out", dest="out", required=True)
    args = ap.parse_args()
    md = open(args.inp, "r", encoding="utf-8").read()
    slides = split_slides(md)
    deck = { "meta": {"template_id": "koerber_2025", "language": "de"}, "slides": slides }
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(deck, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()