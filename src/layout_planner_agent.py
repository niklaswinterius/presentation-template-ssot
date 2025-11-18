
"""
layout_planner_agent.py

Ebene C – Schritt 1:
---------------------
Nimmt
  1) das maschinenlesbare SSOT (JSON)
  2) ein in Ebene B erzeugtes, NORMALISIERTES Inhalts-JSON

und erzeugt einen "slide_plan.json":
  - für jede Folie: gewähltes Layout + Slot-Befüllung.
"""

import argparse
import json
from typing import Dict, Any, List


def load_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def matches_condition(features: Dict[str, Any], condition: Dict[str, Any]) -> bool:
    for key, value in condition.items():
        if key.endswith("_min"):
            feat = key.replace("_min", "")
            if features.get(feat, 0) < value:
                return False
        elif key.endswith("_max"):
            feat = key.replace("_max", "")
            if features.get(feat, 0) > value:
                return False
        elif key.endswith("_in"):
            feat = key.replace("_in", "")
            if features.get(feat) not in value:
                return False
        else:
            if features.get(key) != value:
                return False
    return True


def score_layouts(ssot: Dict[str, Any], features: Dict[str, Any]) -> Dict[str, float]:
    selection_cfg = ssot.get("layout_selection", {})
    default_scores = selection_cfg.get("default_layout_scores", {})
    scores = dict(default_scores)

    for rule in selection_cfg.get("rules", []):
        condition = rule.get("condition", {})
        if matches_condition(features, condition):
            for layout_id, delta in rule.get("layout_scores", {}).items():
                scores[layout_id] = scores.get(layout_id, 0.0) + float(delta)

    return scores


def choose_best_layout(scores: Dict[str, float], ssot: Dict[str, Any]) -> str:
    if not scores:
        return ssot["validation"]["fallback"]["default_layout_id"]
    return max(scores.items(), key=lambda kv: kv[1])[0]


def segment_to_slot_mapping(slide: Dict[str, Any], chosen_layout: str) -> Dict[str, Any]:
    segments = slide.get("segments", [])
    title_text = ""
    subtitle_text = ""
    content_blocks: List[str] = []

    for seg in segments:
        t = seg.get("type")
        txt = (seg.get("text") or "").strip()
        if not txt:
            continue
        if t == "title" and not title_text:
            title_text = txt
        elif t == "subtitle" and not subtitle_text:
            subtitle_text = txt
        else:
            content_blocks.append(txt)

    slot_content = {}

    if title_text:
        slot_content["title_main"] = {"text": title_text}
    if subtitle_text:
        slot_content["subtitle_main"] = {"text": subtitle_text}

    if chosen_layout == "content_single_main":
        merged = "\n\n".join(content_blocks)
        if merged:
            slot_content["content_main"] = {"text": merged}
    elif chosen_layout == "content_two_column":
        if content_blocks:
            slot_content["content_left"] = {"text": content_blocks[0]}
        if len(content_blocks) > 1:
            slot_content["content_right"] = {"text": content_blocks[1]}

    return slot_content


def enforce_char_limits(ssot: Dict[str, Any], slot_content: Dict[str, Any]) -> Dict[str, Any]:
    slots_meta = ssot.get("slots", {})
    result = {}

    for slot_id, payload in slot_content.items():
        meta = slots_meta.get(slot_id, {})
        max_chars = meta.get("max_chars")
        text = payload.get("text", "")
        if isinstance(text, str) and isinstance(max_chars, int) and max_chars > 0:
            if len(text) > max_chars:
                payload = dict(payload)
                payload["text"] = text[:max_chars]
                payload["truncated"] = True
        result[slot_id] = payload

    return result


def build_slide_plan(ssot: Dict[str, Any], deck_semantic: Dict[str, Any]) -> Dict[str, Any]:
    slides_out = []

    for slide in deck_semantic.get("slides", []):
        analysis = slide.get("analysis", {})
        features = {
            "segment_count": analysis.get("segment_count"),
            "dominant_type": analysis.get("dominant_type"),
            "relation_type": analysis.get("relation_type", "single_story"),
            "total_chars": analysis.get("total_chars"),
        }

        scores = score_layouts(ssot, features)
        chosen_layout = choose_best_layout(scores, ssot)
        slot_content_raw = segment_to_slot_mapping(slide, chosen_layout)
        slot_content = enforce_char_limits(ssot, slot_content_raw)

        slides_out.append(
            {
                "id": slide.get("id"),
                "semantic_role": slide.get("semantic_role"),
                "chosen_layout_id": chosen_layout,
                "layout_scores": scores,
                "slots": slot_content,
            }
        )

    return {"meta": deck_semantic.get("meta", {}), "slides": slides_out}


def main():
    parser = argparse.ArgumentParser(description="Layout-Planungs-Agent (Ebene C, Schritt 1)")
    parser.add_argument("--ssot", required=True)
    parser.add_argument("--deck", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    ssot = load_json(args.ssot)
    deck_semantic = load_json(args.deck)
    plan = build_slide_plan(ssot, deck_semantic)

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(plan, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
