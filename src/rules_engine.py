# -*- coding: utf-8 -*-
"""
Deterministischer Evaluator für rules.json.
Order: Hard -> Capacity (Warn) -> Accessibility (nur Platzhalter) -> Scoring -> Tiebreakers -> QA (Platzhalter)
CLI:
  python rules_engine.py --rules rules/rules.json --slide slide.json
"""
import json, os, argparse
from typing import Dict, Any, List, Tuple

class Decision:
    def __init__(self):
        self.candidates: List[Dict[str, Any]] = []
        self.violations: List[Dict[str, Any]] = []
        self.warnings: List[Dict[str, Any]] = []
        self.selected: Dict[str, Any] | None = None

def load_rules(path: str | None = None) -> Dict[str, Any]:
    candidates = [path] if path else ["rules/rules.json", "rules.json"]
    for p in candidates:
        if p and os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f: return json.load(f)
    raise FileNotFoundError("rules.json nicht gefunden (erwartet in rules/ oder Root)")

def intent_allowed(slide: Dict[str, Any], layout_id: str) -> bool:
    if slide.get("intent") == "section" and layout_id in ("content_single_main","content_two_column"):
        return False
    return True

def slots_subset_of_layout(slide: Dict[str, Any], layout_id: str, rules: Dict[str, Any]) -> bool:
    allowed = set(rules.get("slot_ids", []))
    for k in (slide.get("slot_mapping") or {}):
        if k not in allowed:
            return False
    return True

def apply_hard_constraints(slide: Dict[str, Any], layout_id: str, rules: Dict[str, Any]) -> Tuple[bool, List[Dict[str, Any]]]:
    viol = []
    if not intent_allowed(slide, layout_id):
        viol.append({"layout": layout_id, "rule": "HARD-INTENT-LAYOUT-COMPAT"})
    if not slots_subset_of_layout(slide, layout_id, rules):
        viol.append({"layout": layout_id, "rule": "HARD-SLOTS-DEFINED"})
    if not (slide.get("title") or (slide.get("slot_mapping") or {}).get("title_main")):
        viol.append({"layout": layout_id, "rule": "HARD-TITLE-REQUIRED"})
    return (len(viol) == 0), viol

def score_layout(slide: Dict[str, Any], layout_id: str, rules: Dict[str, Any]) -> Tuple[float, List[str]]:
    defaults = rules.get("scoring", {}).get("defaults", {})
    score = float(defaults.get(layout_id, 0))
    applied: List[str] = []
    df = slide.get("derived_features", {}) or {}
    for r in rules.get("scoring", {}).get("rules", []):
        cond = r.get("if", {})
        ok = True
        seg = df.get("segment_count")
        rel = df.get("relation_type")
        dom = df.get("dominant_type")
        if "segment_count" in cond and seg != cond["segment_count"]:
            ok = False
        if cond.get("segment_count_max") is not None and (seg or 0) > cond["segment_count_max"]:
            ok = False
        if cond.get("segment_count_min") is not None and (seg or 0) < cond["segment_count_min"]:
            ok = False
        if "relation_type_in" in cond and rel not in cond["relation_type_in"]:
            ok = False
        if "dominant_type_in" in cond and dom not in cond["dominant_type_in"]:
            ok = False
        if ok:
            delta = r.get("effects", {}).get(layout_id, 0)
            if delta:
                score += float(delta); applied.append(r["id"])
    return score, applied

def decide(slide: Dict[str, Any], rules: Dict[str, Any]) -> Decision:
    d = Decision()
    layouts = rules.get("layout_ids", [])
    for layout in layouts:
        ok, viol = apply_hard_constraints(slide, layout, rules)
        if not ok:
            d.violations.extend(viol); continue
        s, applied = score_layout(slide, layout, rules)
        d.candidates.append({"layout": layout, "score": s, "applied_rules": applied})
    if d.candidates:
        d.candidates.sort(key=lambda x: x["score"], reverse=True)
        d.selected = d.candidates[0]
    return d

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rules", default=None)
    ap.add_argument("--slide", required=False, help="Slide-JSON (optional; sonst Demo-Slide)")
    args = ap.parse_args()
    rules = load_rules(args.rules)
    if args.slide:
        slide = json.load(open(args.slide, "r", encoding="utf-8"))
    else:
        slide = {
            "id": "S02",
            "intent": "comparison",
            "title": "SE80 vs. ADT",
            "derived_features": {"segment_count": 2, "relation_type": "comparison", "total_chars": 900, "dominant_type": "bullets"}
        }
    dec = decide(slide, rules)
    print(json.dumps({
        "selected_layout": dec.selected,
        "candidates": dec.candidates,
        "violations": dec.violations
    }, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
