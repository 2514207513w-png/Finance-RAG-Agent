import pytest
from finance_agent.ingest import split_text

def test_overlap_and_end():
    chunks=split_text("abcdefghi",chunk_size=5,overlap=2)
    assert chunks==["abcde","defgh","ghi"]

def test_reject_bad_overlap():
    with pytest.raises(ValueError):split_text("abc",chunk_size=4,overlap=4)
