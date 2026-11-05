"""Wandelt alle Arbeitsblätter, Infoblätter und das Plakat in material/*.docx in PDFs um (LibreOffice).
Aufruf (aus dem Lernpfad-Ordner):  python3 werkzeuge/pdfs.py
"""
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
dateien = sorted(str(p) for p in (ROOT / "material").glob("*.docx"))
subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", str(ROOT / "material"), *dateien],
               check=True, capture_output=True)
print(f"✓ {len(dateien)} PDFs erzeugt")
