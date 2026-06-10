"""
milestone4_embed_retrieve.py

Milestone 4: Embed Your Chunks and Test Retrieval

Project domain:
    Sawtelle, LA food recommendations

What this script does:
    1. Loads chunks created by milestone3_pipeline.py from data/chunks/chunks.json
    2. Embeds each chunk using sentence-transformers/all-MiniLM-L6-v2
    3. Stores chunk text, embeddings, and metadata in ChromaDB
    4. Provides a retrieval function that returns top-k chunks for a query
    5. Tests retrieval with at least 3 evaluation questions
    6. Prints retrieved chunks with source metadata and distance scores
    7. Saves retrieval test results to data/retrieval_tests/retrieval_test_results.md

Before running:
    pip install sentence-transformers chromadb

How to run:
    python milestone4_embed_retrieve.py

Run a custom query:
    python milestone4_embed_retrieve.py --query "What are good dessert places in Sawtelle?"

Change top-k:
    python milestone4_embed_retrieve.py --top-k 5

Rebuild the ChromaDB collection from scratch:
    python milestone4_embed_retrieve.py --rebuild
"""

from __future__ import annotations

import argparse
import json
import textwrap
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------

DEFAULT_CHUNKS_PATH = Path("data/chunks/chunks.json")
DEFAULT_CHROMA_DIR = Path("chroma_db")
DEFAULT_COLLECTION_NAME = "sawtelle_unofficial_guide"
DEFAULT_EMBEDDING_MODEL = "all-MiniLM-L6-v2"
DEFAULT_TOP_K = 4
DEFAULT_RESULTS_DIR = Path("data/retrieval_tests")


# These match the Evaluation Plan in planning.md.
DEFAULT_TEST_QUERIES = [
    "What restaurants are recommended for ramen in Sawtelle?",
    "What are good dessert or sweet snack places in Sawtelle?",
    "What Sawtelle restaurants are recommended if I do not want ramen, noodles, or sushi?",
    "What vegetarian-friendly food options are mentioned near Sawtelle or Westwood?",
    "Which Sawtelle places do students or locals seem especially excited about or rank highly?",
]


# ---------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------

@dataclass
class RetrievedChunk:
    text: str
    source_file: str
    source_id: str
    chunk_index: int
    char_count: int
    distance: float


# ---------------------------------------------------------------------
# Dependency loading
# ---------------------------------------------------------------------

def import_dependencies():
    """
    Import ChromaDB and SentenceTransformer with a helpful error message.
    """
    try:
        import chromadb
        from sentence_transformers import SentenceTransformer
    except ImportError as exc:
        raise ImportError(
            "Missing dependency. Install Milestone 4 dependencies with:\n\n"
            "    pip install sentence-transformers chromadb\n\n"
            "Then run this script again."
        ) from exc

    return chromadb, SentenceTransformer


# ---------------------------------------------------------------------
# Loading chunks
# ---------------------------------------------------------------------

def load_chunks(chunks_path: Path) -> List[Dict[str, Any]]:
    """
    Load chunks from data/chunks/chunks.json.

    Expected chunk format from milestone3_pipeline.py:
        {
          "id": "...",
          "source_id": "...",
          "source_file": "...",
          "chunk_index": 0,
          "text": "...",
          "char_count": 850
        }
    """
    if not chunks_path.exists():
        raise FileNotFoundError(
            f"Could not find chunks file: {chunks_path}\n\n"
            "Run Milestone 3 first:\n"
            "    python milestone3_pipeline.py"
        )

    chunks = json.loads(chunks_path.read_text(encoding="utf-8"))

    if not isinstance(chunks, list):
        raise ValueError(f"{chunks_path} should contain a list of chunk objects.")

    if not chunks:
        raise ValueError(f"{chunks_path} is empty. Run milestone3_pipeline.py again.")

    required_fields = {"id", "source_id", "source_file", "chunk_index", "text"}
    for i, chunk in enumerate(chunks):
        missing = required_fields - set(chunk.keys())
        if missing:
            raise ValueError(
                f"Chunk at index {i} is missing required fields: {sorted(missing)}"
            )
        if not str(chunk["text"]).strip():
            raise ValueError(f"Chunk at index {i} has empty text.")

    return chunks


# ---------------------------------------------------------------------
# ChromaDB setup
# ---------------------------------------------------------------------

def get_chroma_client(chroma_dir: Path):
    """
    Create a persistent ChromaDB client.

    The database is saved locally in chroma_db/.
    """
    chromadb, _ = import_dependencies()
    chroma_dir.mkdir(parents=True, exist_ok=True)
    return chromadb.PersistentClient(path=str(chroma_dir))


def recreate_collection_if_needed(client, collection_name: str, rebuild: bool):
    """
    Delete collection if --rebuild is passed.
    """
    if not rebuild:
        return

    try:
        client.delete_collection(name=collection_name)
        print(f"Deleted existing ChromaDB collection: {collection_name}")
    except Exception:
        # Chroma raises if the collection does not exist. That is fine.
        print(f"No existing collection named {collection_name} to delete.")


def get_or_create_collection(client, collection_name: str):
    """
    Create or load ChromaDB collection.

    metadata={"hnsw:space": "cosine"} tells Chroma to use cosine distance,
    which is common for sentence-transformer embeddings.
    Lower distance = more similar.
    """
    return client.get_or_create_collection(
        name=collection_name,
        metadata={"hnsw:space": "cosine"},
    )


# ---------------------------------------------------------------------
# Embedding + indexing
# ---------------------------------------------------------------------

def build_vector_store(
    chunks: List[Dict[str, Any]],
    chroma_dir: Path = DEFAULT_CHROMA_DIR,
    collection_name: str = DEFAULT_COLLECTION_NAME,
    embedding_model_name: str = DEFAULT_EMBEDDING_MODEL,
    rebuild: bool = False,
):
    """
    Embed all chunks and store them in ChromaDB.

    Stores:
        - chunk text
        - embedding vector
        - source file
        - source id
        - chunk index
        - character count
    """
    _, SentenceTransformer = import_dependencies()

    print("\nLoading embedding model...")
    print(f"Model: {embedding_model_name}")
    model = SentenceTransformer(embedding_model_name)

    client = get_chroma_client(chroma_dir)
    recreate_collection_if_needed(client, collection_name, rebuild=rebuild)
    collection = get_or_create_collection(client, collection_name)

    ids = [str(chunk["id"]) for chunk in chunks]
    texts = [str(chunk["text"]) for chunk in chunks]

    metadatas = []
    for chunk in chunks:
        metadatas.append(
            {
                "source_file": str(chunk["source_file"]),
                "source_id": str(chunk["source_id"]),
                "chunk_index": int(chunk["chunk_index"]),
                "char_count": int(chunk.get("char_count", len(str(chunk["text"])))),
            }
        )

    print("\nEmbedding chunks...")
    print(f"Number of chunks: {len(texts)}")

    embeddings = model.encode(
        texts,
        show_progress_bar=True,
        convert_to_numpy=True,
        normalize_embeddings=True,
    ).tolist()

    print("\nSaving embeddings to ChromaDB...")
    print(f"Chroma directory: {chroma_dir}")
    print(f"Collection: {collection_name}")

    # Use upsert so rerunning the script updates existing ids instead of failing.
    collection.upsert(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    print(f"Stored {len(ids)} chunks in ChromaDB.")

    return collection, model


# ---------------------------------------------------------------------
# Retrieval
# ---------------------------------------------------------------------

def retrieve(
    query: str,
    collection,
    model,
    top_k: int = DEFAULT_TOP_K,
) -> List[RetrievedChunk]:
    """
    Retrieve top-k most relevant chunks for a query.

    Returns:
        List[RetrievedChunk] with text, metadata, and distance scores.

    Distance interpretation with cosine distance:
        - Lower is better.
        - Scores below ~0.5 are usually stronger.
        - Scores above ~0.6-0.7 may indicate weak or noisy matches.
    """
    query_embedding = model.encode(
        [query],
        convert_to_numpy=True,
        normalize_embeddings=True,
    ).tolist()[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )

    retrieved: List[RetrievedChunk] = []

    docs = results.get("documents", [[]])[0]
    metas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    for doc, metadata, distance in zip(docs, metas, distances):
        retrieved.append(
            RetrievedChunk(
                text=doc,
                source_file=str(metadata.get("source_file", "unknown")),
                source_id=str(metadata.get("source_id", "unknown")),
                chunk_index=int(metadata.get("chunk_index", -1)),
                char_count=int(metadata.get("char_count", len(doc))),
                distance=float(distance),
            )
        )

    return retrieved


# ---------------------------------------------------------------------
# Printing + saving retrieval results
# ---------------------------------------------------------------------

def print_retrieval_results(query: str, retrieved_chunks: List[RetrievedChunk]) -> None:
    """
    Print one query and its retrieved chunks.
    """
    print("\n" + "=" * 100)
    print(f"QUERY: {query}")
    print("=" * 100)

    if not retrieved_chunks:
        print("No chunks retrieved.")
        return

    for rank, chunk in enumerate(retrieved_chunks, start=1):
        print("\n" + "-" * 100)
        print(f"Rank: {rank}")
        print(f"Source file: {chunk.source_file}")
        print(f"Chunk index: {chunk.chunk_index}")
        print(f"Characters: {chunk.char_count}")
        print(f"Distance: {chunk.distance:.4f}")
        print("-" * 100)
        print(chunk.text)

    best_distance = retrieved_chunks[0].distance
    print("\nDistance check:")
    if best_distance <= 0.5:
        print(
            f"Top result distance is {best_distance:.4f}. "
            "This is usually a reasonably strong semantic match."
        )
    elif best_distance <= 0.7:
        print(
            f"Top result distance is {best_distance:.4f}. "
            "This may be a weak/moderate match. Inspect the chunk content carefully."
        )
    else:
        print(
            f"Top result distance is {best_distance:.4f}. "
            "This is likely weak retrieval. Check chunk quality, document content, or query wording."
        )


def format_chunk_for_markdown(rank: int, chunk: RetrievedChunk) -> str:
    """
    Format a retrieved chunk for the saved markdown report.
    """
    snippet = chunk.text.strip()
    return f"""#### Result {rank}

- **Source file:** `{chunk.source_file}`
- **Chunk index:** {chunk.chunk_index}
- **Distance:** {chunk.distance:.4f}

```text
{snippet}
```
"""


def save_retrieval_report(
    query_results: List[tuple[str, List[RetrievedChunk]]],
    output_dir: Path = DEFAULT_RESULTS_DIR,
) -> Path:
    """
    Save retrieval test results to a markdown file for README/reference.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "retrieval_test_results.md"

    lines = []
    lines.append("# Milestone 4 Retrieval Test Results")
    lines.append("")
    lines.append("Embedding model: `sentence-transformers/all-MiniLM-L6-v2`")
    lines.append("")
    lines.append("Vector store: `ChromaDB`")
    lines.append("")
    lines.append("Retrieval method: semantic similarity search")
    lines.append("")
    lines.append("Distance note: lower distance means a stronger match. Distances above ~0.6-0.7 may indicate weaker retrieval.")
    lines.append("")

    for i, (query, retrieved_chunks) in enumerate(query_results, start=1):
        lines.append(f"## Test Query {i}")
        lines.append("")
        lines.append(f"**Query:** {query}")
        lines.append("")

        if not retrieved_chunks:
            lines.append("No chunks retrieved.")
            lines.append("")
            continue

        for rank, chunk in enumerate(retrieved_chunks, start=1):
            lines.append(format_chunk_for_markdown(rank, chunk))

        lines.append("### Manual relevance notes")
        lines.append("")
        lines.append("- Retrieved chunks relevant? `[fill in: yes / partially / no]`")
        lines.append("- Why? `[write 1-2 sentences after inspecting the chunks]`")
        lines.append("")

    output_path.write_text("\n".join(lines), encoding="utf-8")
    return output_path


# ---------------------------------------------------------------------
# Main test runner
# ---------------------------------------------------------------------

def run_default_retrieval_tests(collection, model, top_k: int) -> None:
    """
    Test retrieval with the five evaluation-plan queries.
    """
    query_results = []

    print("\nRunning default retrieval tests from planning.md...")
    print(f"Top-k: {top_k}")

    for query in DEFAULT_TEST_QUERIES:
        retrieved_chunks = retrieve(
            query=query,
            collection=collection,
            model=model,
            top_k=top_k,
        )

        print_retrieval_results(query, retrieved_chunks)
        query_results.append((query, retrieved_chunks))

    report_path = save_retrieval_report(query_results)
    print("\n" + "=" * 100)
    print("Saved retrieval test report:")
    print(report_path)
    print("=" * 100)


def run_custom_query(query: str, collection, model, top_k: int) -> None:
    """
    Run a single custom query from the command line.
    """
    retrieved_chunks = retrieve(
        query=query,
        collection=collection,
        model=model,
        top_k=top_k,
    )
    print_retrieval_results(query, retrieved_chunks)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Milestone 4: Embed chunks in ChromaDB and test semantic retrieval."
    )

    parser.add_argument(
        "--chunks-path",
        type=Path,
        default=DEFAULT_CHUNKS_PATH,
        help="Path to chunks.json from Milestone 3. Default: data/chunks/chunks.json",
    )

    parser.add_argument(
        "--chroma-dir",
        type=Path,
        default=DEFAULT_CHROMA_DIR,
        help="Directory where ChromaDB should persist data. Default: chroma_db",
    )

    parser.add_argument(
        "--collection-name",
        type=str,
        default=DEFAULT_COLLECTION_NAME,
        help=f"ChromaDB collection name. Default: {DEFAULT_COLLECTION_NAME}",
    )

    parser.add_argument(
        "--embedding-model",
        type=str,
        default=DEFAULT_EMBEDDING_MODEL,
        help=f"SentenceTransformer model name. Default: {DEFAULT_EMBEDDING_MODEL}",
    )

    parser.add_argument(
        "--top-k",
        type=int,
        default=DEFAULT_TOP_K,
        help="Number of chunks to retrieve per query. Default: 4",
    )

    parser.add_argument(
        "--query",
        type=str,
        default=None,
        help="Optional custom query. If omitted, runs the default evaluation queries.",
    )

    parser.add_argument(
        "--rebuild",
        action="store_true",
        help="Delete and rebuild the ChromaDB collection before indexing.",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.top_k <= 0:
        raise ValueError("--top-k must be a positive integer.")

    print("Starting Milestone 4 embedding + retrieval pipeline...")

    chunks = load_chunks(args.chunks_path)

    collection, model = build_vector_store(
        chunks=chunks,
        chroma_dir=args.chroma_dir,
        collection_name=args.collection_name,
        embedding_model_name=args.embedding_model,
        rebuild=args.rebuild,
    )

    if args.query:
        run_custom_query(
            query=args.query,
            collection=collection,
            model=model,
            top_k=args.top_k,
        )
    else:
        run_default_retrieval_tests(
            collection=collection,
            model=model,
            top_k=args.top_k,
        )

    print("\nMilestone 4 complete.")
    print("Before moving to Milestone 5, inspect the retrieved chunks.")
    print("Ask: Are the chunks specific, on-topic, and from the right source?")


if __name__ == "__main__":
    main()
