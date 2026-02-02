from __future__ import annotations

import argparse
from pathlib import Path

from .config import PipelineConfig
from .pipeline import ensure_paths, run_pipeline


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Pipeline automático de cortes para vídeos de influência."
    )
    parser.add_argument(
        "--config",
        type=Path,
        required=True,
        help="Caminho para o arquivo JSON de configuração.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = PipelineConfig.load(args.config)
    ensure_paths(config)
    result = run_pipeline(config)
    for clip in result.clips:
        print(
            f"Clip {clip.start:.1f}-{clip.end:.1f}s | score={clip.score:.2f} | {clip.summary}"
        )


if __name__ == "__main__":
    main()
