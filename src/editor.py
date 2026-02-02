from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Iterable

from .segmenter import ClipCandidate


def ensure_output_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def cut_clip(video_path: Path, output_path: Path, start: float, end: float) -> None:
    duration = max(end - start, 0.1)
    command = [
        "ffmpeg",
        "-y",
        "-ss",
        f"{start:.3f}",
        "-i",
        str(video_path),
        "-t",
        f"{duration:.3f}",
        "-c",
        "copy",
        str(output_path),
    ]
    subprocess.run(command, check=True)


def export_clips(
    video_path: Path,
    output_dir: Path,
    clips: Iterable[ClipCandidate],
) -> None:
    ensure_output_dir(output_dir)
    for index, clip in enumerate(clips, start=1):
        filename = f"clip_{index:02d}_{clip.start:.1f}-{clip.end:.1f}.mp4"
        output_path = output_dir / filename
        cut_clip(video_path, output_path, clip.start, clip.end)
