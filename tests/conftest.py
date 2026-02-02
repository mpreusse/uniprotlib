from pathlib import Path

import pytest

FIXTURES = Path(__file__).parent / "files"


@pytest.fixture(params=[
    FIXTURES / "Q9Y261.xml",
    FIXTURES / "Q9Y261_https.xml.gz",
], ids=["xml", "xml.gz"])
def test_file(request) -> Path:
    return request.param
