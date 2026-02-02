from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Sequence

from .transcript import TranscriptSegment


@dataclass(frozen=True)
class ClipCandidate:
    start: float
    end: float
    score: float
    summary: str


def score_text(text: str, keyword_weights: Dict[str, float]) -> float:
    lowered = text.lower()
    score = 0.0
    for keyword, weight in keyword_weights.items():
        if keyword in lowered:
            score += weight
    score += min(len(lowered) / 120.0, 1.0)
    return score


def build_candidates(
    segments: Sequence[TranscriptSegment],
    keyword_weights: Dict[str, float],
    min_duration: float,
    max_duration: float,
) -> List[ClipCandidate]:
    candidates: List[ClipCandidate] = []
    for idx, segment in enumerate(segments):
        start = segment.start
        end = segment.end
        summary_parts = [segment.text]
        score = score_text(segment.text, keyword_weights)
        for next_segment in segments[idx + 1 :]:
            if next_segment.end - start > max_duration:
                break
            end = next_segment.end
            summary_parts.append(next_segment.text)
            score += score_text(next_segment.text, keyword_weights)
            duration = end - start
            if duration >= min_duration:
                candidates.append(
                    ClipCandidate(
                        start=start,
                        end=end,
                        score=score,
                        summary=" ".join(summary_parts),
                    )
                )
    return candidates


def select_top_clips(
    candidates: Iterable[ClipCandidate],
    top_n: int,
) -> List[ClipCandidate]:
    sorted_candidates = sorted(candidates, key=lambda item: item.score, reverse=True)
    selected: List[ClipCandidate] = []
    for candidate in sorted_candidates:
        if len(selected) >= top_n:
            break
        if any(
            overlaps(candidate.start, candidate.end, chosen.start, chosen.end)
            for chosen in selected
        ):
            continue
        selected.append(candidate)
    return selected


def overlaps(start_a: float, end_a: float, start_b: float, end_b: float) -> bool:
    return max(start_a, start_b) < min(end_a, end_b)
