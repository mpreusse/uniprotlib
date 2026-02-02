from __future__ import annotations

import gzip
from collections.abc import Iterator
from pathlib import Path

from lxml import etree

from .models import DbReference, Gene, Organism, Sequence, UniProtEntry

_NS_HTTP = "http://uniprot.org/uniprot"
_NS_HTTPS = "https://uniprot.org/uniprot"


def _detect_namespace(path: Path) -> str:
    """Detect which namespace variant a UniProt XML file uses.

    Single-entry downloads use http://, bulk FTP downloads use https://.
    """
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rb") as f:  # type: ignore[arg-type]
        chunk = f.read(2048)
    if b"https://uniprot.org/uniprot" in chunk:
        return _NS_HTTPS
    return _NS_HTTP


def _tag(ns: str, name: str) -> str:
    return f"{{{ns}}}{name}"


def _parse_gene(ns: str, entry: etree._Element) -> Gene | None:
    gene_elem = entry.find(_tag(ns, "gene"))
    if gene_elem is None:
        return None

    primary = None
    synonyms: list[str] = []
    ordered_locus: list[str] = []
    orfs: list[str] = []

    for name_elem in gene_elem.findall(_tag(ns, "name")):
        name_type = name_elem.attrib.get("type")
        text = name_elem.text or ""
        if name_type == "primary":
            primary = text
        elif name_type == "synonym":
            synonyms.append(text)
        elif name_type == "ordered locus":
            ordered_locus.append(text)
        elif name_type == "ORF":
            orfs.append(text)

    return Gene(
        primary=primary,
        synonyms=synonyms,
        ordered_locus_names=ordered_locus,
        orf_names=orfs,
    )


def _parse_organism(ns: str, entry: etree._Element) -> Organism:
    org_elem = entry.find(_tag(ns, "organism"))

    scientific_name = None
    common_name = None
    tax_id = None
    lineage: list[str] = []

    if org_elem is not None:
        for name_elem in org_elem.findall(_tag(ns, "name")):
            name_type = name_elem.attrib.get("type")
            if name_type == "scientific":
                scientific_name = name_elem.text
            elif name_type == "common":
                common_name = name_elem.text

        tax_ref = org_elem.find(
            f"{_tag(ns, 'dbReference')}[@type='NCBI Taxonomy']"
        )
        if tax_ref is not None:
            tax_id = tax_ref.attrib.get("id")

        lineage_elem = org_elem.find(_tag(ns, "lineage"))
        if lineage_elem is not None:
            lineage = [
                t.text or ""
                for t in lineage_elem.findall(_tag(ns, "taxon"))
            ]

    return Organism(
        scientific_name=scientific_name,
        common_name=common_name,
        tax_id=tax_id,
        lineage=lineage,
    )


def _parse_sequence(ns: str, entry: etree._Element) -> Sequence:
    seq_elem = entry.find(_tag(ns, "sequence"))
    raw = seq_elem.text or ""
    value = raw.replace("\n", "").replace(" ", "")

    return Sequence(
        value=value,
        length=int(seq_elem.attrib.get("length", 0)),
        mass=int(seq_elem.attrib.get("mass", 0)),
        checksum=seq_elem.attrib.get("checksum", ""),
    )


def _parse_db_references(ns: str, entry: etree._Element) -> list[DbReference]:
    refs: list[DbReference] = []
    for elem in entry.findall(_tag(ns, "dbReference")):
        molecule_elem = elem.find(_tag(ns, "molecule"))
        molecule = molecule_elem.attrib.get("id") if molecule_elem is not None else None

        properties = {
            prop.attrib["type"]: prop.attrib["value"]
            for prop in elem.findall(_tag(ns, "property"))
        }

        refs.append(DbReference(
            type=elem.attrib["type"],
            id=elem.attrib["id"],
            molecule=molecule,
            properties=properties,
        ))
    return refs


def _parse_entry(ns: str, entry: etree._Element) -> UniProtEntry:
    accessions = [
        acc.text or ""
        for acc in entry.findall(_tag(ns, "accession"))
    ]

    names = entry.findall(_tag(ns, "name"))
    entry_name = names[0].text or "" if names else ""

    protein_name = None
    name_elem = entry.find(
        f"{_tag(ns, 'protein')}/{_tag(ns, 'recommendedName')}/{_tag(ns, 'fullName')}"
    )
    if name_elem is not None:
        protein_name = name_elem.text

    keywords = [
        kw.text or ""
        for kw in entry.findall(_tag(ns, "keyword"))
    ]

    pe_elem = entry.find(_tag(ns, "proteinExistence"))
    protein_existence = pe_elem.attrib.get("type") if pe_elem is not None else None

    return UniProtEntry(
        primary_accession=accessions[0] if accessions else "",
        accessions=accessions,
        entry_name=entry_name,
        dataset=entry.attrib.get("dataset", ""),
        protein_name=protein_name,
        gene=_parse_gene(ns, entry),
        organism=_parse_organism(ns, entry),
        sequence=_parse_sequence(ns, entry),
        keywords=keywords,
        db_references=_parse_db_references(ns, entry),
        protein_existence=protein_existence,
    )


def _parse_single_file(path: Path) -> Iterator[UniProtEntry]:
    ns = _detect_namespace(path)
    opener = gzip.open if path.suffix == ".gz" else open

    with opener(path, "rb") as f:  # type: ignore[arg-type]
        context = etree.iterparse(f, events=("end",), tag=_tag(ns, "entry"))

        for _event, entry in context:
            yield _parse_entry(ns, entry)

            # memory cleanup — critical for multi-GB files
            entry.clear()
            while entry.getprevious() is not None:
                del entry.getparent()[0]


def parse_xml(*paths: str | Path) -> Iterator[UniProtEntry]:
    """Stream-parse one or more UniProt XML files, yielding UniProtEntry objects.

    Accepts plain XML or gzip-compressed files (auto-detected from ``.gz``
    extension). Handles both namespace variants (``http://`` for single-entry
    web downloads, ``https://`` for bulk FTP dumps). Files are processed
    sequentially. Memory stays bounded regardless of file size.

    Args:
        *paths: One or more file paths (str or Path) to UniProt XML files.

    Yields:
        UniProtEntry for each ``<entry>`` element in the XML.

    Raises:
        ValueError: If no paths are provided.

    Example::

        from uniprotlib import parse_xml

        for entry in parse_xml("uniprot_sprot.xml.gz"):
            print(entry.primary_accession, entry.organism.scientific_name)
    """
    if not paths:
        raise ValueError("At least one path is required")

    for p in paths:
        yield from _parse_single_file(Path(p))
