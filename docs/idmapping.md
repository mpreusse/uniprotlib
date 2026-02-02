# ID Mapping

UniProt provides tab-separated ID mapping files (`idmapping.dat`) that map UniProt accessions to identifiers in external databases. These files are available for the full database or per organism.

The `parse_idmapping` function streams these files and yields one `IdMapping` per line:

```python
from uniprotlib import parse_idmapping

for m in parse_idmapping("idmapping.dat.gz"):
    print(m.accession, m.id_type, m.id)
```

## Filtering by database type

Use `id_type` to extract only the mappings you need. This is the common case — e.g., getting all UniProt-to-NCBI-Gene mappings:

```python
for m in parse_idmapping("idmapping.dat.gz", id_type="GeneID"):
    print(m.accession, m.id)

for m in parse_idmapping("idmapping.dat.gz", id_type="RefSeq"):
    print(m.accession, m.id)
```

Non-matching lines are skipped without constructing objects, so filtering is efficient even on multi-GB files.

## Common ID types

| `id_type` value | Database |
|---|---|
| `GeneID` | NCBI Gene (Entrez Gene) |
| `RefSeq` | NCBI RefSeq protein |
| `RefSeq_NT` | NCBI RefSeq nucleotide |
| `EMBL` | EMBL/GenBank/DDBJ |
| `EMBL-CDS` | EMBL CDS |
| `PDB` | Protein Data Bank |
| `GI` | NCBI GI number |
| `UniRef100` | UniRef 100% cluster |
| `UniRef90` | UniRef 90% cluster |
| `UniRef50` | UniRef 50% cluster |
| `KEGG` | KEGG |
| `NCBI_TaxID` | NCBI Taxonomy |

See the [UniProt ID mapping README](https://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/idmapping/README) for the full list.

## Converting to a dictionary

A common pattern is building a lookup dictionary from the stream:

```python
from collections import defaultdict
from uniprotlib import parse_idmapping

# UniProt accession -> list of Gene IDs
uniprot_to_gene = defaultdict(list)
for m in parse_idmapping("idmapping.dat.gz", id_type="GeneID"):
    uniprot_to_gene[m.accession].append(m.id)
```
