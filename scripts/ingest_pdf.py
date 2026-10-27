"""Import a local public PDF to data/chunks.json (careful: overwrites file)."""
import argparse
import json
from pathlib import Path
from finance_agent.ingest import parse_local_pdf

def main():
    p=argparse.ArgumentParser()
    p.add_argument("pdf",type=Path)
    p.add_argument("--product-code",required=True)
    p.add_argument("--document-id",required=True)
    p.add_argument("--out",type=Path,default=Path("output/chunks.json"))
    args=p.parse_args()
    chunks=parse_local_pdf(args.pdf,args.product_code,args.document_id)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(chunks,ensure_ascii=False,indent=2),encoding="utf-8")
    print(f"Generated {len(chunks)} chunks at {args.out}. For demo index, copy reviewed chunks to data/chunks.json")

if __name__=="__main__": main()
