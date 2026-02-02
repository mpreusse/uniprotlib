from dataclasses import dataclass


@dataclass(slots=True)
class Organism:
    """Organism annotation from a UniProt entry.

    Attributes:
        scientific_name: Binomial name, e.g. ``"Homo sapiens"``.
        common_name: Vernacular name, e.g. ``"Human"``. None if not annotated.
        tax_id: NCBI Taxonomy identifier as a string, e.g. ``"9606"``.
        lineage: Taxonomic lineage from root to most specific taxon,
            e.g. ``["Eukaryota", ..., "Homo"]``.
    """

    scientific_name: str | None
    common_name: str | None
    tax_id: str | None
    lineage: list[str]


@dataclass(slots=True)
class Gene:
    """Gene names associated with a UniProt entry.

    Attributes:
        primary: Primary gene name, e.g. ``"FOXA2"``. None if not annotated.
        synonyms: Alternative gene names, e.g. ``["HNF3B", "TCF3B"]``.
        ordered_locus_names: Systematic locus identifiers, e.g. ``["b0001"]``.
        orf_names: Open reading frame identifiers.
    """

    primary: str | None
    synonyms: list[str]
    ordered_locus_names: list[str]
    orf_names: list[str]


@dataclass(slots=True)
class Sequence:
    """Protein amino acid sequence.

    Attributes:
        value: Amino acid string (no whitespace), e.g. ``"MLGAVKMEG..."``.
        length: Number of amino acids.
        mass: Molecular mass in Daltons.
        checksum: CRC64 checksum of the sequence.
    """

    value: str
    length: int
    mass: int
    checksum: str


@dataclass(slots=True)
class DbReference:
    """Cross-reference to an external database.

    Attributes:
        type: Database name, e.g. ``"PDB"``, ``"RefSeq"``, ``"EMBL"``.
        id: Identifier in that database, e.g. ``"7YZE"``.
        molecule: Isoform identifier, e.g. ``"Q9Y261-1"``. None if not
            isoform-specific.
        properties: Additional key-value properties, e.g.
            ``{"method": "X-ray", "resolution": "1.99 A"}``.
    """

    type: str
    id: str
    molecule: str | None
    properties: dict[str, str]


@dataclass(slots=True)
class IdMapping:
    """Single row from a UniProt idmapping.dat file.

    Each row maps a UniProt accession to one identifier in an external database.

    Attributes:
        accession: UniProtKB accession, e.g. ``"Q6GZX4"``.
        id_type: Database name, e.g. ``"GeneID"``, ``"RefSeq"``, ``"EMBL"``.
        id: Identifier in that database, e.g. ``"YP_031579.1"``.
    """

    accession: str
    id_type: str
    id: str


@dataclass(slots=True)
class UniProtEntry:
    """A single UniProtKB entry parsed from XML.

    Attributes:
        primary_accession: Primary accession, e.g. ``"Q9Y261"``.
        accessions: All accessions including primary and secondary.
        entry_name: Mnemonic entry name, e.g. ``"FOXA2_HUMAN"``.
        dataset: ``"Swiss-Prot"`` or ``"TrEMBL"``.
        protein_name: Recommended full protein name. None if not annotated.
        gene: Gene names. None if the entry has no gene annotation.
        organism: Source organism with taxonomy.
        sequence: Amino acid sequence with metadata.
        keywords: UniProt keywords, e.g. ``["Activator", "Nucleus"]``.
        db_references: Cross-references to external databases.
    """

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
