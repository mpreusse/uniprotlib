# UniProt XML

The `parse_xml` function streams UniProt XML files and yields one `UniProtEntry` per protein record. It handles files of any size with bounded memory.

```python
from uniprotlib import parse_xml

for entry in parse_xml("uniprot_sprot.xml.gz"):
    print(entry.primary_accession, entry.protein_name)
```

## Gzip support

Gzip-compressed files are detected automatically from the `.gz` extension:

```python
# both work the same way
for entry in parse_xml("Q9Y261.xml"):
    ...

for entry in parse_xml("uniprot_sprot.xml.gz"):
    ...
```

## Multiple files

Pass multiple paths to process them sequentially:

```python
for entry in parse_xml("human.xml.gz", "mouse.xml.gz"):
    print(entry.primary_accession, entry.organism.scientific_name)
```

## Accessing fields

Each `UniProtEntry` contains nested dataclasses:

```python
entry = next(parse_xml("Q9Y261.xml"))

# basic metadata
entry.primary_accession  # "Q9Y261"
entry.entry_name          # "FOXA2_HUMAN"
entry.dataset             # "Swiss-Prot"
entry.protein_name        # "Hepatocyte nuclear factor 3-beta"

# gene (can be None)
if entry.gene:
    entry.gene.primary    # "FOXA2"
    entry.gene.synonyms   # ["HNF3B", "TCF3B"]

# organism
entry.organism.scientific_name  # "Homo sapiens"
entry.organism.tax_id           # "9606"
entry.organism.lineage          # ["Eukaryota", ..., "Homo"]

# sequence
entry.sequence.value     # "MLGAVKMEG..."
entry.sequence.length    # 457
entry.sequence.mass      # 48306

# keywords
entry.keywords  # ["Activator", "Nucleus", ...]

# database cross-references
for ref in entry.db_references:
    print(ref.type, ref.id)  # "PDB", "7YZE"
```

## Namespace handling

UniProt XML files use different namespace URIs depending on the source:

- `http://uniprot.org/uniprot` — single-entry web downloads
- `https://uniprot.org/uniprot` — bulk FTP downloads

The parser detects the namespace automatically. No configuration needed.
