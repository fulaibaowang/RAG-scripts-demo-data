#!/usr/bin/env python3
"""Generate docs_chunked.jsonl from docs.jsonl with docno = \"{pmid}#abstract\".

Preserves all fields; overwrites or sets docno to the chunk-style id.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--input",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "data" / "docs.jsonl",
        help="Source corpus JSONL (default: ../data/docs.jsonl)",
    )
    ap.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "data" / "docs_chunked.jsonl",
        help="Output JSONL (default: ../data/docs_chunked.jsonl)",
    )
    args = ap.parse_args()

    n = 0
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.input.open("r", encoding="utf-8") as fin, args.output.open(
        "w", encoding="utf-8"
    ) as fout:
        for line in fin:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            pmid = rec.get("pmid")
            if pmid is None:
                raise ValueError(f"Record missing pmid: keys={list(rec.keys())[:8]}")
            rec["docno"] = f"{str(pmid).strip()}#abstract"
            fout.write(json.dumps(rec, ensure_ascii=False) + "\n")
            n += 1
    print(f"[make_docs_chunked] wrote {n} lines -> {args.output}")


if __name__ == "__main__":
    main()
