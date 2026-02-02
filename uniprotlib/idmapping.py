from __future__ import annotations

import gzip
from collections.abc import Iterator
from pathlib import Path

from .models import IdMapping


def _open_file(path: Path):
    if path.suffix == ".gz":
        return gzip.open(path, "rt", encoding="utf-8")
    return open(path, encoding="utf-8")


def _parse_single_file(
    path: Path, id_type: str | None,
) -> Iterator[IdMapping]:
    with _open_file(path) as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if len(parts) != 3:
                continue
            if id_type is not None and parts[1] != id_type:
                continue
            yield IdMapping(accession=parts[0], id_type=parts[1], id=parts[2])


def parse_idmapping(
    *paths: str | Path, id_type: str | None = None,
) -> Iterator[IdMapping]:
    """Stream-parse one or more UniProt idmapping.dat files, yielding IdMapping objects.

    Accepts plain text or gzip-compressed files (auto-detected from .gz extension).
    Optionally filter to a single database type with id_type.
    """
    if not paths:
        raise ValueError("At least one path is required")

    for p in paths:
        yield from _parse_single_file(Path(p), id_type)
