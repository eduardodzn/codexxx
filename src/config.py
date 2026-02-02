from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict


DEFAULT_KEYWORD_WEIGHTS: Dict[str, float] = {
    "segredo": 2.0,
    "incrível": 1.5,
    "viral": 1.2,
    "atenção": 1.2,
    "dica": 1.0,
    "errado": 1.0,
    "cuidado": 1.0,
    "resultado": 1.0,
}


@dataclass
class PipelineConfig:
    video_path: Path
    transcript_path: Path
    output_dir: Path
    min_clip_duration: float = 10.0
    max_clip_duration: float = 45.0
    top_n: int = 5
    keyword_weights: Dict[str, float] = field(
        default_factory=lambda: dict(DEFAULT_KEYWORD_WEIGHTS)
    )

    @classmethod
    def load(cls, path: Path) -> "PipelineConfig":
        data = json.loads(path.read_text(encoding="utf-8"))
        return cls(
            video_path=Path(data["video_path"]),
            transcript_path=Path(data["transcript_path"]),
            output_dir=Path(data["output_dir"]),
            min_clip_duration=float(data.get("min_clip_duration", 10.0)),
            max_clip_duration=float(data.get("max_clip_duration", 45.0)),
            top_n=int(data.get("top_n", 5)),
            keyword_weights={
                **DEFAULT_KEYWORD_WEIGHTS,
                **data.get("keyword_weights", {}),
            },
        )
