from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List

from .config import PipelineConfig
from .editor import export_clips
from .segmenter import ClipCandidate, build_candidates, select_top_clips
from .transcript import iter_non_empty_segments, load_whisper_json


@dataclass(frozen=True)
class PipelineResult:
    clips: List[ClipCandidate]


def run_pipeline(config: PipelineConfig) -> PipelineResult:
    segments = load_whisper_json(config.transcript_path)
    segments = iter_non_empty_segments(segments)
    candidates = build_candidates(
        segments,
        keyword_weights=config.keyword_weights,
        min_duration=config.min_clip_duration,
        max_duration=config.max_clip_duration,
    )
    selected = select_top_clips(candidates, top_n=config.top_n)
    export_clips(config.video_path, config.output_dir, selected)
    return PipelineResult(clips=selected)


def ensure_paths(config: PipelineConfig) -> None:
    missing: List[Path] = []
    for path in (config.video_path, config.transcript_path):
        if not path.exists():
            missing.append(path)
    if missing:
        missing_list = ", ".join(str(path) for path in missing)
        raise FileNotFoundError(f"Arquivos não encontrados: {missing_list}")
