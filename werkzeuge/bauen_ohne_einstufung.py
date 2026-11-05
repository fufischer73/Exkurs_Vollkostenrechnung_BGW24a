"""Baut Web-Version und Moodle-Kurs ohne Einstufungstests: jede Stufe öffnet nur nach der Abgabe des Meilensteins davor.

Der Lernpfad-Baukasten koppelt die Einstufungstests an die Freischaltung „einstufung“. Dieses Skript arbeitet deshalb mit einer
temporären Kopie der Baukasten-Skripte, in der die Einstufungstests abgeschaltet sind. Der Baukasten selbst bleibt unverändert.

Aufruf (aus dem Lernpfad-Ordner):  python3 werkzeuge/bauen_ohne_einstufung.py <pfad-zum-baukasten> [--moodle 4|5]
"""
import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("baukasten", type=Path)
ap.add_argument("--moodle", default="4")
args = ap.parse_args()
root = Path(__file__).resolve().parent.parent
with tempfile.TemporaryDirectory() as tmp:
    ziel = Path(tmp) / "skripte"
    shutil.copytree(args.baukasten / "skripte", ziel)
    shutil.copytree(args.baukasten / "vorlage", Path(tmp) / "vorlage")
    for extra in ("referenzen",):
        if (args.baukasten / extra).exists():
            shutil.copytree(args.baukasten / extra, Path(tmp) / extra)
    g = ziel / "gemeinsam.py"
    text = g.read_text(encoding="utf-8")
    alt = 'return (self.moodle.get("freischaltung", "einstufung") == "einstufung") and len(self.stufen) > 1'
    assert alt in text, "Baukasten-Version nicht erkannt"
    g.write_text(text.replace(alt, "return False  # Einstufungstests abgeschaltet (Lernpfad Vollkostenrechnung)"), encoding="utf-8")
    for skript, extra in (("pruefen.py", []), ("bauen.py", []), ("durchklicken.py", ["--nur-links"]), ("moodle_kurs.py", ["--moodle", args.moodle])):
        r = subprocess.run([sys.executable, str(ziel / skript), str(root), *extra])
        if r.returncode:
            sys.exit(r.returncode)
