# uniprotlib

> **Note:** This library was vibe coded with Claude. It works, it's tested, but review accordingly.

Python library for parsing UniProt XML files. Handles both single-entry downloads and multi-GB gzip-compressed database dumps with bounded memory usage.

## Installation

```bash
pip install uniprotlib
```

Or with [uv](https://docs.astral.sh/uv/):

```bash
uv add uniprotlib
```

## Usage

```python
from uniprotlib import parse_xml

# single file
for entry in parse_xml("Q9Y261.xml"):
    print(entry.primary_accession, entry.protein_name)

# gzipped bulk download
for entry in parse_xml("uniprot_sprot.xml.gz"):
    print(entry.gene.primary, entry.organism.scientific_name)

# multiple files
for entry in parse_xml("human.xml.gz", "mouse.xml.gz"):
    print(entry.primary_accession)
```

`parse_xml()` returns an iterator that yields `UniProtEntry` objects. Gzip detection is automatic based on the `.gz` extension. Memory stays bounded regardless of file size.

## Parsed fields

| Model | Fields |
|---|---|
| `UniProtEntry` | primary_accession, accessions, entry_name, dataset, protein_name, gene, organism, sequence, keywords, db_references |
| `Gene` | primary, synonyms, ordered_locus_names, orf_names |
| `Organism` | scientific_name, common_name, tax_id, lineage |
| `Sequence` | value, length, mass, checksum |
| `DbReference` | type, id, molecule, properties |

All model classes are dataclasses with full type annotations and `py.typed` support.

## Development

Requires Python >= 3.12 and [uv](https://docs.astral.sh/uv/).

```bash
uv sync
uv run pytest tests/ -v
```

## License

MIT
