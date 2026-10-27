"""Stdlib-only entrypoint for users who cannot install dependencies yet."""
from pathlib import Path
import ast, json
root=Path(__file__).resolve().parents[1]
files=list(root.rglob("*.py"))
for file in files:
    ast.parse(file.read_text(encoding="utf-8"),filename=str(file))
for file in (root/"data").glob("*.json"):
    json.loads(file.read_text(encoding="utf-8"))
print(f"Package structure OK: {len(files)} Python files; JSON files parse correctly.")
print("Next: pip install -r requirements.txt && python -m scripts.demo")
