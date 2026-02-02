# uniprotlib

Python library for parsing UniProt XML files and ID mapping data. Handles both single-entry downloads and multi-GB gzip-compressed database dumps with bounded memory usage.

## Installation

```bash
pip install uniprotlib
```

Or with [uv](https://docs.astral.sh/uv/):

```bash
uv add uniprotlib
```

## Quick start

### Parse UniProt XML

```python
from uniprotlib import parse_xml

for entry in parse_xml("uniprot_sprot.xml.gz"):
    print(entry.primary_accession, entry.protein_name)
    print(entry.organism.scientific_name, entry.organism.tax_id)
```

### Parse ID mappings

```python
from uniprotlib import parse_idmapping

for m in parse_idmapping("idmapping.dat.gz", id_type="GeneID"):
    print(m.accession, m.id)
```

See the [UniProt XML](xml.md) and [ID Mapping](idmapping.md) usage guides for more examples, or the [API Reference](api.md) for full details.
