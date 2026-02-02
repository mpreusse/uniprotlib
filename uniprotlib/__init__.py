from .models import DbReference, Gene, Organism, Sequence, UniProtEntry
from .parser import parse_xml

__all__ = [
    "DbReference",
    "Gene",
    "Organism",
    "Sequence",
    "UniProtEntry",
    "parse_xml",
]
