from .idmapping import parse_idmapping
from .models import DbReference, Gene, IdMapping, Organism, Sequence, UniProtEntry
from .parser import parse_xml

__all__ = [
    "DbReference",
    "Gene",
    "IdMapping",
    "Organism",
    "Sequence",
    "UniProtEntry",
    "parse_idmapping",
    "parse_xml",
]
