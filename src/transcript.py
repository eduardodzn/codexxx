from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List


@dataclass(frozen=True)
class TranscriptSegment:
    start: float
    end: float
    text: str


def load_whisper_json(path: Path) -> List[TranscriptSegment]:
    data = json.loads(path.read_text(encoding="utf-8"))
    segments = data.get("segments", [])
    return [
        TranscriptSegment(
            start=float(segment["start"]),
            end=float(segment["end"]),
            text=str(segment.get("text", "")).strip(),
        )
        for segment in segments
    ]


def iter_non_empty_segments(segments: Iterable[TranscriptSegment]) -> List[TranscriptSegment]:
    return [segment for segment in segments if segment.text]
