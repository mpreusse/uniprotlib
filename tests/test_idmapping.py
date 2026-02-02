import gzip
from pathlib import Path

from uniprotlib import IdMapping, parse_idmapping

FILES = Path(__file__).parent / "files"
DAT = FILES / "idmapping.dat"


def test_total_rows():
    rows = list(parse_idmapping(DAT))
    assert len(rows) == 46


def test_returns_idmapping_dataclass():
    row = next(iter(parse_idmapping(DAT)))
    assert isinstance(row, IdMapping)


def test_first_row():
    row = next(iter(parse_idmapping(DAT)))
    assert row.accession == "Q6GZX4"
    assert row.id_type == "UniProtKB-ID"
    assert row.id == "001R_FRG3G"


def test_accessions():
    accessions = sorted({r.accession for r in parse_idmapping(DAT)})
    assert accessions == ["Q197F8", "Q6GZX3", "Q6GZX4"]


def test_duplicate_id_type():
    gi = [r for r in parse_idmapping(DAT) if r.accession == "Q6GZX4" and r.id_type == "GI"]
    assert len(gi) == 2
    assert gi[0].id == "49237298"
    assert gi[1].id == "81941549"


def test_filter_id_type():
    rows = list(parse_idmapping(DAT, id_type="RefSeq"))
    assert len(rows) == 3
    assert all(r.id_type == "RefSeq" for r in rows)
    assert rows[0].id == "YP_031579.1"


def test_filter_id_type_no_match():
    rows = list(parse_idmapping(DAT, id_type="NoSuchDB"))
    assert rows == []


def test_gzip(tmp_path):
    gz_path = tmp_path / "idmapping.dat.gz"
    with open(DAT, "rb") as f_in, gzip.open(gz_path, "wb") as f_out:
        f_out.write(f_in.read())

    plain = list(parse_idmapping(DAT))
    compressed = list(parse_idmapping(gz_path))
    assert plain == compressed


def test_multiple_files():
    rows = list(parse_idmapping(DAT, DAT))
    assert len(rows) == 92
