from dataclasses import dataclass


@dataclass(slots=True)
class Organism:
    scientific_name: str | None
    common_name: str | None
    tax_id: str | None
    lineage: list[str]


@dataclass(slots=True)
class Gene:
    primary: str | None
    synonyms: list[str]
    ordered_locus_names: list[str]
    orf_names: list[str]


@dataclass(slots=True)
class Sequence:
    value: str
    length: int
    mass: int
    checksum: str


@dataclass(slots=True)
class DbReference:
    type: str
    id: str
    molecule: str | None
    properties: dict[str, str]


@dataclass(slots=True)
class IdMapping:
    accession: str
    id_type: str
    id: str


@dataclass(slots=True)
class UniProtEntry:
    primary_accession: str
    accessions: list[str]
    entry_name: str
    dataset: str
    protein_name: str | None
    gene: Gene | None
    organism: Organism
    sequence: Sequence
    keywords: list[str]
    db_references: list[DbReference]
