from pathlib import Path

from uniprot_tools import parse_xml


def test_accessions(test_file: Path):
    entries = list(parse_xml(test_file))
    assert len(entries) == 1
    entry = entries[0]
    assert entry.primary_accession == "Q9Y261"
    assert entry.accessions == ["Q9Y261", "Q8WUW4", "Q96DF7"]


def test_entry_metadata(test_file: Path):
    entries = list(parse_xml(test_file))
    assert len(entries) == 1
    entry = entries[0]
    assert entry.entry_name == "FOXA2_HUMAN"
    assert entry.dataset == "Swiss-Prot"


def test_protein_name(test_file: Path):
    entries = list(parse_xml(test_file))
    assert len(entries) == 1
    entry = entries[0]
    assert entry.protein_name == "Hepatocyte nuclear factor 3-beta"


def test_gene(test_file: Path):
    entries = list(parse_xml(test_file))
    assert len(entries) == 1
    entry = entries[0]
    gene = entry.gene
    assert gene is not None
    assert gene.primary == "FOXA2"
    assert gene.synonyms == ["HNF3B", "TCF3B"]
    assert gene.ordered_locus_names == []
    assert gene.orf_names == []


def test_organism(test_file: Path):
    entries = list(parse_xml(test_file))
    assert len(entries) == 1
    entry = entries[0]
    org = entry.organism
    assert org.scientific_name == "Homo sapiens"
    assert org.common_name == "Human"
    assert org.tax_id == "9606"
    assert org.lineage[0] == "Eukaryota"
    assert org.lineage[-1] == "Homo"
    assert len(org.lineage) == 14


def test_sequence(test_file: Path):
    entries = list(parse_xml(test_file))
    assert len(entries) == 1
    entry = entries[0]
    seq = entry.sequence
    assert seq.length == 457
    assert seq.mass == 48306
    assert seq.checksum == "61DDE4C75C70680A"
    assert seq.value.startswith("MLGAVKMEG")
    assert seq.value.endswith("PIMNSS")
    assert len(seq.value) == 457


def test_keywords(test_file: Path):
    entries = list(parse_xml(test_file))
    assert len(entries) == 1
    entry = entries[0]
    kw = entry.keywords
    assert len(kw) == 13
    assert "3D-structure" in kw
    assert "Activator" in kw
    assert "Nucleus" in kw


def test_db_references(test_file: Path):
    entries = list(parse_xml(test_file))
    assert len(entries) == 1
    entry = entries[0]
    refs = entry.db_references
    assert len(refs) == 143

    # simple reference (no properties, no molecule)
    alphafold = [r for r in refs if r.type == "AlphaFoldDB"]
    assert len(alphafold) == 1
    assert alphafold[0].id == "Q9Y261"
    assert alphafold[0].molecule is None
    assert alphafold[0].properties == {}

    # reference with properties
    pdb = [r for r in refs if r.type == "PDB" and r.id == "7YZE"]
    assert len(pdb) == 1
    assert pdb[0].properties["method"] == "X-ray"
    assert pdb[0].properties["resolution"] == "1.99 A"
    assert pdb[0].properties["chains"] == "A=149-273"

    # reference with molecule (isoform)
    ccds = [r for r in refs if r.type == "CCDS" and r.id == "CCDS13147.1"]
    assert len(ccds) == 1
    assert ccds[0].molecule == "Q9Y261-1"

    # reference with molecule + properties
    refseq = [r for r in refs if r.type == "RefSeq" and r.id == "NP_068556.2"]
    assert len(refseq) == 1
    assert refseq[0].molecule == "Q9Y261-2"
    assert refseq[0].properties["nucleotide sequence ID"] == "NM_021784.5"


def test_multiple_files():
    files_dir = Path(__file__).parent / "files"
    entries = list(parse_xml(
        files_dir / "Q9Y261.xml",
        files_dir / "Q9Y261_https.xml.gz",
    ))
    assert len(entries) == 2
    assert entries[0].primary_accession == "Q9Y261"
    assert entries[1].primary_accession == "Q9Y261"
