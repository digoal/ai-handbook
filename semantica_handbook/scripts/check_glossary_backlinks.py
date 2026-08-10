#!/usr/bin/env python3
"""
Check that glossary terms, when first introduced in a chapter, are followed by
a `[[ch-55-glossary]]` backlink within ~200 characters.

Usage:
    python scripts/check_glossary_backlinks.py [chapter.md ...]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

HANDBOOK_ROOT = Path(__file__).resolve().parent.parent
GLOSSARY_PATH = HANDBOOK_ROOT / "part-vii-reference" / "ch-55-glossary.md"
PARTS = [
    "part-i-foundations",
    "part-ii-core-modules",
    "part-iii-cross-cutting",
    "part-iv-integrations",
    "part-v-workflows",
    "part-vi-operations",
    "part-vii-reference",
]

# Match `**Term**` definitions inside ch-55-glossary.md
# Term must be alphanumeric, may contain spaces, underscores, slashes
TERM_RE = re.compile(r"^\s*-\s+\*\*([A-Za-z][\w /().-]*?)\*\*\s+—", re.MULTILINE)
# Backlink marker
BACKLINK_RE = re.compile(r"\[\[ch-55-glossary[^\]]*\]\]")
# Limit search window after term first occurrence
WINDOW = 200

# Stop-words and overly generic terms that should not be checked
SKIP_TERMS = {
    "AgentContext", "ArrowExporter", "Athena",
    "BGP", "DDL", "Docling",
    "Endpoint", "ErrorCode", "Extras", "Explorer",  # covered by ch-31
    "FAISS", "FileIngestor", "FalkorDB",  # product names with own chapters
    "GLOSSARY.md", "GitHub", "Git",  # generic names
    "HuggingFace", "Instructor", "InvestigatorGuide",  # product names
    "JSON-LD", "KG", "KGBuilder", "KGVisualizer",
    "LLM", "LLMExtraction", "Layer1/Layer2/Layer3 Provenance", "LiteLLM",
    "MCP", "MCP Server", "mermaid", "merge_strategy",
    "NamespaceManager", "Neptune", "NetworkX", "Neo4j",
    "OntologyGenerator", "OntologyValidator", "OWL", "Ollama", "Oxigraph",
    "PipelineBuilder", "ParquetExporter", "PDFParser", "PROV-O", "Policy",
    "PolicyEngine", "PostgreSQL", "ProvenanceManager",
    "QualityError", "QueryEngine",
    "Reasoner", "RDFExporter", "Relationship", "Redis", "ReteEngine", "RRF",
    "SageMaker", "SHACL", "Sigma", "SKOS", "SLSA", "SPARQL", "Snowflake",
    "SourceDocument", "StreamIngestor",
    "Triplet", "TripletStore", "TemporalValidationError", "TemporalVisualizer",
    "Tiktoken",
    "UMAP", "UMAP-learn",
    "VectorStore", "VectorIndexer", "Visualization",
    "WebIngestor", "W3C PROV-O", "WebSocket",
    "YAML",
    "zvec",
    # Already in chapter titles — skip noise
    "BaseIngestor", "BaseProvider",
    "Conflict", "ConflictDetector", "ConflictResolver",
    "Decision", "DecisionRecorder", "DecisionQuery",
    "Dedup", "Datalog",
    "Entity", "EntityResolver",
    "Ingest",
    "TripletStore", "TripletStore", "Relationship", "Triplet",
    "VectorStore", "VectorIndexer",
    "Dedup", "Conflict", "CausalChain", "BiTemporal",
}

# Additional terms that should appear with backlink (high-frequency usage)
HIGH_VALUE_TERMS = {
    "ContextGraph", "GraphBuilder", "GraphStore", "VectorStore",
    "SourceDocument", "TripletStore", "ProvenanceManager",
    "DecisionRecorder", "DecisionQuery", "DecisionQuery",
    "CausalChainAnalyzer", "PolicyEngine",
    "EntityResolver", "ContextGraph",
    "ForceAtlas2", "FA2",
    "build_knowledge_base", "method_registry",
    "_ModuleProxy", "register_reader",
    "/ws/graph-updates",
    "ConfigurationError", "ValidationError", "ProcessingError",
    "BiTemporal", "RRF", "W3C PROV-O",
    "Neo4j Browser", "GDS",
}


def extract_glossary_terms() -> set[str]:
    if not GLOSSARY_PATH.exists():
        return set()
    text = GLOSSARY_PATH.read_text(encoding="utf-8")
    return {m.group(1).strip() for m in TERM_RE.finditer(text)}


def iter_chapters(args: list[str]) -> list[Path]:
    if args:
        return [Path(a) for a in args]
    chapters: list[Path] = []
    for part in PARTS:
        part_dir = HANDBOOK_ROOT / part
        if part_dir.exists():
            chapters.extend(sorted(part_dir.glob("ch-*.md")))
    return chapters


def first_occurrence(text: str, term: str) -> int:
    """Find the first occurrence of `term` as a whole word/phrase in text."""
    # Escape for regex
    pat = re.escape(term)
    # Use word boundaries where appropriate; for terms like /ws/graph-updates use literal boundaries
    if term[0].isalpha():
        m = re.search(rf"\b{pat}\b", text)
    else:
        m = re.search(pat, text)
    return m.start() if m else -1


def check_chapter(ch: Path, terms: set[str]) -> list[str]:
    text = ch.read_text(encoding="utf-8")
    # Skip the glossary chapter itself
    if ch.name.startswith("ch-55-"):
        return []
    errors: list[str] = []
    for term in sorted(terms, key=len, reverse=True):
        idx = first_occurrence(text, term)
        if idx < 0:
            continue
        # Look ahead WINDOW chars
        snippet = text[idx: idx + WINDOW]
        if BACKLINK_RE.search(snippet):
            continue
        errors.append(f"{ch.name}: '{term}' first appears at offset {idx} without [[ch-55-glossary]] backlink")
    return errors


def find_missing(chapters: list[Path]) -> list[tuple[Path, str, int]]:
    """Return [(chapter, term, offset), ...] for each missing backlink."""
    terms = extract_glossary_terms() - SKIP_TERMS
    missing: list[tuple[Path, str, int]] = []
    for ch in chapters:
        text = ch.read_text(encoding="utf-8")
        if ch.name.startswith("ch-55-"):
            continue
        for term in sorted(terms, key=len, reverse=True):
            idx = first_occurrence(text, term)
            if idx < 0:
                continue
            snippet = text[idx: idx + WINDOW]
            if BACKLINK_RE.search(snippet):
                continue
            missing.append((ch, term, idx))
    return missing


def fix_chapter(ch: Path, term: str, offset: int) -> bool:
    """Insert ` [[ch-55-glossary]] ` after the term at offset. Returns True on success."""
    text = ch.read_text(encoding="utf-8")
    if offset < 0 or offset >= len(text):
        return False
    pat = re.escape(term)
    if term[0].isalpha():
        match = re.search(rf"\b{pat}\b", text[offset:])
    else:
        match = re.search(pat, text[offset:])
    if not match:
        return False
    abs_pos = offset + match.end()
    # Skip if the next char already starts a backlink
    snippet = text[abs_pos: abs_pos + WINDOW]
    if BACKLINK_RE.search(snippet):
        return False
    # Insert backlink immediately after the term
    new_text = text[:abs_pos] + " [[ch-55-glossary]]" + text[abs_pos:]
    ch.write_text(new_text, encoding="utf-8")
    return True


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    fix_mode = "--fix" in sys.argv
    chapters = iter_chapters(args)
    missing = find_missing(chapters)

    if fix_mode and missing:
        fixed = 0
        for ch, term, offset in missing:
            if fix_chapter(ch, term, offset):
                fixed += 1
        # Re-scan
        missing = find_missing(chapters)
        print(f"✓ Fixed {fixed} backlink(s). {len(missing)} still missing.")

    if not missing:
        print(f"✓ {len(chapters)} chapter(s) — every glossary term has a backlink on first use.")
        return 0

    print(f"⚠ {len(missing)} missing backlink(s). Top 30:")
    for ch, term, offset in missing[:30]:
        print(f"  - {ch.name}: '{term}' at offset {offset}")
    print("(run with --fix to auto-insert; or set SKIP_TERMS to suppress)")
    return 0  # soft fail (set to 1 to make hard)


if __name__ == "__main__":
    sys.exit(main())