"""
Milestone 3: Document Ingestion + Cleaning + Chunking Pipeline

Project domain:
    Sawtelle, LA food recommendations

What this script does:
    1. Loads all .txt documents from data/raw/
    2. Saves raw text copies to data/processed/raw_snapshots/
    3. Cleans each document by removing HTML, boilerplate, URLs, extra whitespace, etc.
    4. Saves cleaned documents to data/processed/cleaned/
    5. Splits cleaned documents into paragraph-aware chunks
    6. Saves all chunks to data/chunks/chunks.json and data/chunks/chunks.jsonl
    7. Prints one cleaned document and 5 representative chunks for manual inspection

How to run:
    python milestone3_pipeline.py

Expected project structure:
    project/
    ├── data/
    │   ├── raw/
    │   │   ├── source1.txt
    │   │   ├── source2.txt
    │   │   └── ...
    │   ├── processed/
    │   └── chunks/
    └── milestone3_pipeline.py
"""

from __future__ import annotations

import argparse
import html
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, List


DEFAULT_RAW_DIR = Path("data/raw")
DEFAULT_PROCESSED_DIR = Path("data/processed")
DEFAULT_CHUNKS_DIR = Path("data/chunks")

# From your planning.md: paragraph-aware chunks around 700–900 characters
# with about 150 characters of overlap.
DEFAULT_CHUNK_SIZE = 850
DEFAULT_OVERLAP = 150
MIN_CHUNK_CHARS = 120


@dataclass
class Document:
    source_id: str
    source_file: str
    raw_text: str
    cleaned_text: str


@dataclass
class Chunk:
    id: str
    source_id: str
    source_file: str
    chunk_index: int
    text: str
    char_count: int


def load_txt_documents(raw_dir: Path) -> List[tuple[Path, str]]:
    """Load all .txt files from the raw documents folder."""
    if not raw_dir.exists():
        raise FileNotFoundError(
            f"Could not find raw document folder: {raw_dir}\n"
            "Create it with: mkdir -p data/raw\n"
            "Then add your .txt source documents there."
        )

    txt_files = sorted(raw_dir.glob("*.txt"))
    if not txt_files:
        raise FileNotFoundError(
            f"No .txt files found in {raw_dir}.\n"
            "Milestone 3 expects your collected source documents as plain .txt files."
        )

    loaded = []
    for file_path in txt_files:
        text = file_path.read_text(encoding="utf-8", errors="replace")
        loaded.append((file_path, text))

    return loaded


def save_raw_snapshot(source_path: Path, raw_text: str, raw_snapshot_dir: Path) -> None:
    """Save an unchanged copy of the raw text before cleaning."""
    raw_snapshot_dir.mkdir(parents=True, exist_ok=True)
    output_path = raw_snapshot_dir / source_path.name
    output_path.write_text(raw_text, encoding="utf-8")


def remove_boilerplate_lines(text: str) -> str:
    """Remove common navigation, cookie, and social boilerplate lines."""
    boilerplate_patterns = [
        r"^\s*log in\s*$",
        r"^\s*sign up\s*$",
        r"^\s*subscribe\s*$",
        r"^\s*advertisement\s*$",
        r"^\s*read more\s*$",
        r"^\s*share\s*$",
        r"^\s*save\s*$",
        r"^\s*hide\s*$",
        r"^\s*report\s*$",
        r"^\s*reply\s*$",
        r"^\s*cookie policy\s*$",
        r"^\s*privacy policy\s*$",
        r"^\s*terms of use\s*$",
        r"^\s*all rights reserved.*$",
        r"^\s*skip to main content\s*$",
        r"^\s*open menu\s*$",
        r"^\s*close menu\s*$",
        r"^\s*comments?\s*$",
        r"^\s*\d+\s+comments?\s*$",
        r"^\s*sort by:.*$",
    ]

    cleaned_lines = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            cleaned_lines.append("")
            continue

        should_remove = any(
            re.match(pattern, stripped, flags=re.IGNORECASE)
            for pattern in boilerplate_patterns
        )
        if not should_remove:
            cleaned_lines.append(stripped)

    return "\n".join(cleaned_lines)


def clean_text(text: str) -> str:
    """
    Clean a raw document.

    Removes obvious noise while keeping restaurant names, opinions,
    ratings, dish descriptions, and Sawtelle/Westwood context.
    """
    # Decode HTML entities: &amp; -> &, &nbsp; -> space, etc.
    text = html.unescape(text)
    text = text.replace("\xa0", " ")

    # Remove script/style blocks if copied from webpages.
    text = re.sub(
        r"<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>",
        " ",
        text,
        flags=re.IGNORECASE,
    )
    text = re.sub(
        r"<style\b[^<]*(?:(?!<\/style>)<[^<]*)*<\/style>",
        " ",
        text,
        flags=re.IGNORECASE,
    )

    # Remove remaining HTML tags.
    text = re.sub(r"<[^>]+>", " ", text)

    # Convert Markdown links [text](url) -> text.
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)

    # Remove bare URLs. Keep URLs in planning.md/source metadata, not retrieval text.
    text = re.sub(r"https?://\S+", " ", text)
    text = re.sub(r"www\.\S+", " ", text)

    # Remove common social counters.
    text = re.sub(
        r"\b\d+\s+(upvotes?|downvotes?|shares?)\b",
        " ",
        text,
        flags=re.IGNORECASE,
    )

    # Remove obvious navigation/boilerplate lines.
    text = remove_boilerplate_lines(text)

    # Normalize spacing while preserving paragraph breaks.
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    lines = [line.strip() for line in text.splitlines()]
    return "\n".join(lines).strip()


def build_documents(raw_items: List[tuple[Path, str]], processed_dir: Path) -> List[Document]:
    """Create Document objects and save raw snapshots + cleaned documents."""
    raw_snapshot_dir = processed_dir / "raw_snapshots"
    cleaned_dir = processed_dir / "cleaned"
    cleaned_dir.mkdir(parents=True, exist_ok=True)

    documents: List[Document] = []
    for source_path, raw_text in raw_items:
        save_raw_snapshot(source_path, raw_text, raw_snapshot_dir)
        cleaned = clean_text(raw_text)

        cleaned_path = cleaned_dir / source_path.name
        cleaned_path.write_text(cleaned, encoding="utf-8")

        documents.append(
            Document(
                source_id=source_path.stem,
                source_file=source_path.name,
                raw_text=raw_text,
                cleaned_text=cleaned,
            )
        )

    return documents


def split_into_paragraphs(text: str) -> List[str]:
    """Split text into cleaned paragraphs."""
    paragraphs = re.split(r"\n\s*\n", text)
    cleaned_paragraphs = []

    for para in paragraphs:
        para = para.strip()
        para = re.sub(r"\s+", " ", para)
        if para:
            cleaned_paragraphs.append(para)

    return cleaned_paragraphs


def split_long_text(text: str, max_chars: int, overlap: int) -> List[str]:
    """Split a very long paragraph with a sentence-aware fallback."""
    if len(text) <= max_chars:
        return [text]

    chunks = []
    start = 0

    while start < len(text):
        target_end = min(start + max_chars, len(text))
        window = text[start:target_end]

        # Prefer ending near a sentence boundary.
        split_candidates = [
            window.rfind(". "),
            window.rfind("! "),
            window.rfind("? "),
            window.rfind("; "),
        ]
        best_split = max(split_candidates)

        if best_split > int(max_chars * 0.55):
            end = start + best_split + 1
        else:
            end = target_end

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break

        start = max(0, end - overlap)

    return chunks


def chunk_document(
    document: Document,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    overlap: int = DEFAULT_OVERLAP,
    min_chunk_chars: int = MIN_CHUNK_CHARS,
) -> List[Chunk]:
    """
    Paragraph-aware chunking.

    Strategy:
        - Add paragraphs until the chunk approaches chunk_size.
        - Split very long paragraphs using sentence-aware fallback.
        - Add overlap from the previous chunk so context is not lost.
        - Drop tiny fragments unless they are the only content in a document.
    """
    paragraphs = split_into_paragraphs(document.cleaned_text)
    chunk_texts: List[str] = []
    current_parts: List[str] = []
    current_len = 0

    for paragraph in paragraphs:
        if len(paragraph) > chunk_size:
            if current_parts:
                chunk_texts.append("\n\n".join(current_parts).strip())
                current_parts = []
                current_len = 0

            chunk_texts.extend(split_long_text(paragraph, chunk_size, overlap))
            continue

        projected_len = current_len + len(paragraph) + (2 if current_parts else 0)

        if projected_len <= chunk_size:
            current_parts.append(paragraph)
            current_len = projected_len
        else:
            if current_parts:
                chunk_texts.append("\n\n".join(current_parts).strip())

            previous_tail = ""
            if chunk_texts and overlap > 0:
                previous_tail = chunk_texts[-1][-overlap:].strip()
                first_space = previous_tail.find(" ")
                if first_space != -1 and first_space < 30:
                    previous_tail = previous_tail[first_space + 1 :].strip()

            if previous_tail:
                current_parts = [previous_tail, paragraph]
                current_len = len(previous_tail) + len(paragraph) + 2
            else:
                current_parts = [paragraph]
                current_len = len(paragraph)

    if current_parts:
        chunk_texts.append("\n\n".join(current_parts).strip())

    filtered = [c for c in chunk_texts if len(c.strip()) >= min_chunk_chars]
    if not filtered and chunk_texts:
        filtered = [max(chunk_texts, key=len)]

    chunks: List[Chunk] = []
    for i, text in enumerate(filtered):
        text = text.strip()
        chunks.append(
            Chunk(
                id=f"{document.source_id}_{i:04d}",
                source_id=document.source_id,
                source_file=document.source_file,
                chunk_index=i,
                text=text,
                char_count=len(text),
            )
        )

    return chunks


def chunk_all_documents(
    documents: Iterable[Document],
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    overlap: int = DEFAULT_OVERLAP,
) -> List[Chunk]:
    """Chunk every document and return one flat list."""
    all_chunks: List[Chunk] = []
    for document in documents:
        all_chunks.extend(chunk_document(document, chunk_size, overlap))
    return all_chunks


def save_chunks(chunks: List[Chunk], chunks_dir: Path) -> None:
    """Save chunks in JSON and JSONL formats."""
    chunks_dir.mkdir(parents=True, exist_ok=True)
    chunk_dicts = [asdict(chunk) for chunk in chunks]

    json_path = chunks_dir / "chunks.json"
    json_path.write_text(
        json.dumps(chunk_dicts, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    jsonl_path = chunks_dir / "chunks.jsonl"
    with jsonl_path.open("w", encoding="utf-8") as f:
        for chunk in chunk_dicts:
            f.write(json.dumps(chunk, ensure_ascii=False) + "\n")


def save_summary(documents: List[Document], chunks: List[Chunk], processed_dir: Path) -> None:
    """Save a simple milestone summary file for README.md."""
    summary_path = processed_dir / "milestone3_summary.txt"

    chunks_by_source = {}
    for chunk in chunks:
        chunks_by_source.setdefault(chunk.source_file, 0)
        chunks_by_source[chunk.source_file] += 1

    lines = [
        "Milestone 3 Summary",
        "===================",
        "",
        f"Documents loaded: {len(documents)}",
        f"Total chunks created: {len(chunks)}",
        f"Chunk size target: {DEFAULT_CHUNK_SIZE} characters",
        f"Overlap: {DEFAULT_OVERLAP} characters",
        "",
        "Chunks by source:",
    ]

    for source_file, count in sorted(chunks_by_source.items()):
        lines.append(f"- {source_file}: {count} chunks")

    summary_path.write_text("\n".join(lines), encoding="utf-8")


def print_cleaned_document_sample(documents: List[Document], max_chars: int = 1200) -> None:
    """Print one cleaned document for manual inspection."""
    if not documents:
        return

    doc = documents[0]
    print("\n" + "=" * 80)
    print("CLEANED DOCUMENT SAMPLE")
    print("=" * 80)
    print(f"Source: {doc.source_file}")
    print("-" * 80)
    print(doc.cleaned_text[:max_chars])
    if len(doc.cleaned_text) > max_chars:
        print("\n...[truncated]")
    print("=" * 80)


def print_representative_chunks(chunks: List[Chunk], sample_size: int = 5) -> None:
    """Print 5 representative chunks for manual inspection."""
    if not chunks:
        print("No chunks available to inspect.")
        return

    print("\n" + "=" * 80)
    print(f"{min(sample_size, len(chunks))} REPRESENTATIVE CHUNKS FOR INSPECTION")
    print("=" * 80)

    if len(chunks) <= sample_size:
        selected = chunks
    else:
        indices = [round(i * (len(chunks) - 1) / (sample_size - 1)) for i in range(sample_size)]
        selected = [chunks[i] for i in indices]

    for chunk in selected:
        print("\n" + "-" * 80)
        print(f"Chunk ID: {chunk.id}")
        print(f"Source: {chunk.source_file}")
        print(f"Chunk index: {chunk.chunk_index}")
        print(f"Characters: {chunk.char_count}")
        print("-" * 80)
        print(chunk.text)

    print("\n" + "=" * 80)
    print("Inspection questions:")
    print("1. Does each chunk make sense on its own?")
    print("2. Could someone answer a question from this chunk without reading nearby chunks?")
    print("3. Are there HTML artifacts, menus, ads, cookie banners, or empty strings?")
    print("4. Are chunks too small and fragment-like, or too large with unrelated topics?")
    print("=" * 80)


def print_chunk_count_guidance(total_chunks: int) -> None:
    """Print milestone guidance about total chunk count."""
    print("\n" + "=" * 80)
    print("CHUNK COUNT CHECK")
    print("=" * 80)
    print(f"Total chunks created: {total_chunks}")

    if total_chunks < 50:
        print(
            "Warning: You have fewer than 50 chunks. For 10+ documents, this may mean "
            "your chunks are too large or your source documents do not contain enough "
            "substantive text yet."
        )
    elif total_chunks > 2000:
        print(
            "Warning: You have more than 2,000 chunks. This may mean your chunks are "
            "too small, which can make retrieval noisy."
        )
    else:
        print(
            "Chunk count is in the expected range. Still inspect the sample chunks "
            "manually before moving to embeddings."
        )

    print("=" * 80)


def run_pipeline(
    raw_dir: Path,
    processed_dir: Path,
    chunks_dir: Path,
    chunk_size: int,
    overlap: int,
) -> None:
    """Run the full Milestone 3 pipeline."""
    print("Starting Milestone 3 document pipeline...")
    print(f"Raw directory: {raw_dir}")
    print(f"Processed directory: {processed_dir}")
    print(f"Chunks directory: {chunks_dir}")
    print(f"Chunk size: {chunk_size}")
    print(f"Overlap: {overlap}")

    raw_items = load_txt_documents(raw_dir)
    print(f"\nLoaded {len(raw_items)} raw .txt documents.")

    documents = build_documents(raw_items, processed_dir)
    print(f"Cleaned and saved {len(documents)} documents.")

    chunks = chunk_all_documents(documents, chunk_size=chunk_size, overlap=overlap)
    save_chunks(chunks, chunks_dir)
    save_summary(documents, chunks, processed_dir)

    print("Saved chunks to:")
    print(f"- {chunks_dir / 'chunks.json'}")
    print(f"- {chunks_dir / 'chunks.jsonl'}")
    print("Saved summary to:")
    print(f"- {processed_dir / 'milestone3_summary.txt'}")

    print_cleaned_document_sample(documents)
    print_representative_chunks(chunks, sample_size=5)
    print_chunk_count_guidance(len(chunks))

    print("\nMilestone 3 pipeline complete.")
    print("Before moving to Milestone 4, manually inspect the printed chunks and saved files.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Milestone 3 ingestion, cleaning, and chunking pipeline.")

    parser.add_argument("--raw-dir", type=Path, default=DEFAULT_RAW_DIR)
    parser.add_argument("--processed-dir", type=Path, default=DEFAULT_PROCESSED_DIR)
    parser.add_argument("--chunks-dir", type=Path, default=DEFAULT_CHUNKS_DIR)
    parser.add_argument("--chunk-size", type=int, default=DEFAULT_CHUNK_SIZE)
    parser.add_argument("--overlap", type=int, default=DEFAULT_OVERLAP)

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    if args.overlap >= args.chunk_size:
        raise ValueError("Overlap must be smaller than chunk size.")

    run_pipeline(
        raw_dir=args.raw_dir,
        processed_dir=args.processed_dir,
        chunks_dir=args.chunks_dir,
        chunk_size=args.chunk_size,
        overlap=args.overlap,
    )
