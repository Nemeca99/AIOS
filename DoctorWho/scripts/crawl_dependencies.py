#!/usr/bin/env python3
"""
Dependency crawler for AIOS_Clean
- Start from an entrypoint (e.g., HiveMind/luna_main.py)
- Resolve local imports transitively within the repository
- Scan each discovered file for placeholder markers (YOUR_, CHANGEME, placeholder, TODO, NotImplementedError)
- NEW: Detect runtime file loads by scanning for open()/json.load()/Path usage pointing at .json/.yaml/.yml/.txt
- Print a concise report of dependencies and findings
- Optional: emit GraphViz DOT graph of dependencies via --dot
- Optional: emit JSON via --json
"""

import os
import re
import sys
import json
import argparse
from pathlib import Path
from typing import Set, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]
PLACEHOLDER_PATTERNS = re.compile(r"YOUR_|CHANGEME|placeholder|TODO|NotImplementedError", re.IGNORECASE)
PY_IMPORT_RE = re.compile(r"^\s*from\s+([\w\.]+)\s+import|^\s*import\s+([\w\.]+)")
RUNTIME_FILE_RE = re.compile(r"['\"]([^'\"]+\.(?:json|ya?ml|txt))['\"]")

# Map module name -> file path cache
module_cache: Dict[str, Path] = {}


def is_local_module(module: str) -> bool:
    top = module.split(".")[0]
    return (ROOT / top).exists()


def resolve_module_to_path(module: str) -> Path:
    if module in module_cache:
        return module_cache[module]
    parts = module.split(".")
    candidate = ROOT.joinpath(*parts).with_suffix(".py")
    if candidate.exists():
        module_cache[module] = candidate
        return candidate
    candidate = ROOT.joinpath(*parts, "__init__.py")
    if candidate.exists():
        module_cache[module] = candidate
        return candidate
    module_cache[module] = None
    return None


def parse_imports(py_path: Path) -> List[str]:
    imports: List[str] = []
    try:
        for line in py_path.read_text(encoding="utf-8", errors="ignore").splitlines():
            m = PY_IMPORT_RE.match(line)
            if not m:
                continue
            mod = m.group(1) or m.group(2)
            if mod:
                imports.append(mod)
    except Exception:
        pass
    return imports


def detect_runtime_files(py_path: Path) -> List[str]:
    found: List[str] = []
    try:
        text = py_path.read_text(encoding="utf-8", errors="ignore")
        for m in RUNTIME_FILE_RE.finditer(text):
            rel = m.group(1)
            if rel.startswith("http://") or rel.startswith("https://"):
                continue
            found.append(rel)
    except Exception:
        pass
    return found


def crawl(entry: Path) -> Tuple[List[Path], Dict[str, Set[str]]]:
    seen: Set[Path] = set()
    queue: List[Path] = [entry]
    ordered: List[Path] = []
    edges: Dict[str, Set[str]] = {}

    while queue:
        cur = queue.pop(0)
        if not cur or cur in seen or not cur.exists() or cur.suffix != ".py":
            continue
        seen.add(cur)
        ordered.append(cur)
        cur_key = str(cur.relative_to(ROOT))
        edges.setdefault(cur_key, set())

        for mod in parse_imports(cur):
            if not is_local_module(mod):
                continue
            resolved = resolve_module_to_path(mod)
            if resolved and resolved not in seen:
                queue.append(resolved)
            if resolved:
                edges[cur_key].add(str(resolved.relative_to(ROOT)))

    return ordered, edges


def scan_placeholders(path: Path) -> List[Tuple[int, str]]:
    matches: List[Tuple[int, str]] = []
    try:
        for i, line in enumerate(path.read_text(encoding="utf-8", errors="ignore").splitlines(), start=1):
            if PLACEHOLDER_PATTERNS.search(line):
                matches.append((i, line.strip()))
    except Exception:
        pass
    return matches


def main():
    parser = argparse.ArgumentParser(description="AIOS dependency crawler")
    parser.add_argument("entry", nargs="?", default=str(ROOT / "HiveMind" / "luna_main.py"), help="Entry python file")
    parser.add_argument("--dot", dest="dot", default=None, help="Write DOT graph to this path")
    parser.add_argument("--json", dest="json_out", default=None, help="Write JSON report to this path")
    args = parser.parse_args()

    entry = Path(args.entry)
    if not entry.exists():
        print(f"❌ Entry file not found: {entry}")
        sys.exit(1)

    print(f"🔎 Crawling from entry: {entry.relative_to(ROOT)}")
    deps, edges = crawl(entry)
    print(f"📄 Files discovered: {len(deps)}\n")

    report = []
    total_findings = 0
    runtime_files: Dict[str, List[str]] = {}

    for p in deps:
        findings = scan_placeholders(p)
        total_findings += len(findings)
        rf = detect_runtime_files(p)
        runtime_files[str(p.relative_to(ROOT))] = rf
        report.append({
            "file": str(p.relative_to(ROOT)),
            "findings": findings[:10],
            "findings_count": len(findings),
            "runtime_files": rf
        })

    print("=== Dependency Report ===")
    for item in report:
        print(f"- {item['file']} : {item['findings_count']} findings")
        for (ln, text) in item["findings"]:
            print(f"   L{ln}: {text[:140]}")
        if item["runtime_files"]:
            print(f"   Runtime files: {item['runtime_files']}")
    print("=========================")
    print(f"Total placeholder/TODO findings: {total_findings}")

    if args.json_out:
        Path(args.json_out).write_text(json.dumps({"total": total_findings, "report": report, "edges": {k: list(v) for k, v in edges.items()}}, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"📄 JSON written: {args.json_out}")

    if args.dot:
        with open(args.dot, "w", encoding="utf-8") as f:
            f.write("digraph aios {\n")
            f.write("  rankdir=LR;\n  node [shape=box, fontsize=10];\n")
            for src, tgts in edges.items():
                for tgt in tgts:
                    f.write(f'  "{src}" -> "{tgt}";\n')
            for src, files in runtime_files.items():
                for rf in files:
                    f.write(f'  "{src}" -> "{rf}" [style=dashed, color=gray];\n')
            f.write("}\n")
        print(f"🗺️  DOT graph written to: {args.dot}")


if __name__ == "__main__":
    main()
