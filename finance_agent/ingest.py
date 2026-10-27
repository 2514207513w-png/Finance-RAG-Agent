"""Local educational PDF ingestion helper. No OCR and no remote URLs."""
from pathlib import Path
from typing import Iterable

def split_text(text:str,chunk_size:int=650,overlap:int=100)->list[str]:
    if not 0 <= overlap < chunk_size: raise ValueError("overlap must be in [0, chunk_size)")
    text=" ".join(text.split())
    if not text:return []
    out=[]
    step=chunk_size-overlap
    for start in range(0,len(text),step):
        out.append(text[start:start+chunk_size])
        if start+chunk_size>=len(text):break
    return out

def parse_local_pdf(pdf_path:Path, product_code:str,document_id:str)->list[dict]:
    from pypdf import PdfReader
    chunks=[]
    for number,page in enumerate(PdfReader(str(pdf_path)).pages,start=1):
        for part in split_text(page.extract_text() or ""):
            chunks.append({"product_code":product_code,"document_id":document_id,"page":number,"text":part})
    return chunks
