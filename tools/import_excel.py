"""Read source rows and hyperlink targets from XLSX, without modifying the workbook."""
from __future__ import annotations

import argparse
import hashlib
import json
import posixpath
import re
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

NS = {"s": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
RID = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"


def https(value: str) -> str:
    value = value.strip()
    if value and not re.match(r"^https?://", value):
        value = "https://" + value
    if value and not value.startswith("https://"):
        raise ValueError(f"Only HTTPS source URLs are accepted: {value}")
    return value


def extract(path: Path) -> dict:
    rows, blanks = [], []
    with zipfile.ZipFile(path) as archive:
        strings = []
        if "xl/sharedStrings.xml" in archive.namelist():
            strings = ["".join(t.text or "" for t in item.iterfind(".//s:t", NS))
                       for item in ET.fromstring(archive.read("xl/sharedStrings.xml"))]
        rels = {r.attrib["Id"]: r.attrib["Target"] for r in
                ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))}
        workbook = ET.fromstring(archive.read("xl/workbook.xml"))
        for sheet in workbook.find("s:sheets", NS):
            target = rels[sheet.attrib[RID]]
            name = target.lstrip("/") if target.startswith("/") else posixpath.normpath("xl/" + target)
            root = ET.fromstring(archive.read(name))
            relpath = posixpath.join(posixpath.dirname(name), "_rels", posixpath.basename(name) + ".rels")
            sheetrels = {r.attrib["Id"]: r.attrib["Target"] for r in
                         ET.fromstring(archive.read(relpath))} if relpath in archive.namelist() else {}
            links = {}
            for link in root.findall(".//s:hyperlink", NS):
                reference = link.attrib["ref"]
                ends = reference.split(":")
                start, stop = [int(re.search(r"\d+", cell).group()) for cell in (ends[0], ends[-1])]
                column = re.match(r"[A-Z]+", ends[0]).group()
                for number in range(start, stop + 1):
                    links[f"{column}{number}"] = sheetrels.get(link.attrib.get(RID), "")
            for row in root.findall("s:sheetData/s:row", NS):
                n = int(row.attrib["r"])
                if n == 1:
                    continue
                cells = {}
                for cell in row:
                    value = cell.find("s:v", NS)
                    text = value.text or "" if value is not None else "".join(t.text or "" for t in cell.iterfind(".//s:t", NS))
                    if cell.attrib.get("t") == "s":
                        text = strings[int(text)]
                    cells[re.match(r"[A-Z]+", cell.attrib["r"]).group()] = text.strip()
                url = links.get(f"C{n}") or cells.get("C", "")
                if not url:
                    if cells.get("A"):
                        blanks.append({"sheet": sheet.attrib["name"], "row": n, "number": cells["A"]})
                    continue
                repository = links.get(f"B{n}") or cells.get("B", "")
                if repository and "/" in repository and not repository.startswith("http"):
                    repository = "https://github.com/" + repository
                rows.append({"sheet": sheet.attrib["name"], "row": n, "number": cells.get("A", ""),
                             "repository": repository, "url": https(url),
                             "category": cells.get("D", ""), "usage": cells.get("E", "")})
    return {"workbook": path.name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "sources": rows, "blank_rows": blanks}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workbook", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = extract(args.workbook)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"Imported {len(result['sources'])} source URLs; {len(result['blank_rows'])} blank numbered rows ignored.")
