"""
app.py

Milestone 5: Grounded Generation + Query Interface

Project domain:
    Sawtelle, LA food recommendations

What this script does:
    1. Loads the existing ChromaDB vector store from Milestone 4
    2. Retrieves the top-k relevant chunks for a user question
    3. Sends ONLY those retrieved chunks to Groq's LLM
    4. Forces the LLM to answer only from retrieved context
    5. Programmatically appends source attribution
    6. Provides a Gradio web interface

Before running:
    1. Make sure Milestone 3 has created:
        data/chunks/chunks.json

    2. Make sure Milestone 4 has created:
        chroma_db/

    3. Install dependencies:
        pip install groq python-dotenv gradio sentence-transformers chromadb

    4. Add your Groq key to .env:
        GROQ_API_KEY=your_key_here

How to run the web app:
    python app.py

Then open:
    http://localhost:7860

How to test from command line:
    python app.py --cli "What are good ramen places in Sawtelle?"
"""

from __future__ import annotations

import argparse
import os
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Any

import chromadb
import gradio as gr
from dotenv import load_dotenv
from groq import Groq
from sentence_transformers import SentenceTransformer


# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------


CHROMA_DIR = Path("chroma_db")
COLLECTION_NAME = "sawtelle_unofficial_guide"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
GROQ_MODEL = "llama-3.3-70b-versatile"

DEFAULT_TOP_K = 4

# If the best retrieved chunk has a distance above this threshold,
# the retrieval is likely weak. The app will refuse to answer instead
# of letting the LLM make something up.
MAX_DISTANCE_FOR_ANSWER = 0.75

REFUSAL_MESSAGE = (
    "I don't have enough information from the provided documents to answer that."
)


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
    citation_id: str


# ---------------------------------------------------------------------
# Initialization
# ---------------------------------------------------------------------

def load_groq_client() -> Groq:
    """
    Load Groq client using GROQ_API_KEY from .env.
    """
    load_dotenv()

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise RuntimeError(
            "Missing GROQ_API_KEY.\n\n"
            "Create a .env file in your project root and add:\n"
            "GROQ_API_KEY=your_key_here"
        )

    return Groq(api_key=api_key)


def load_embedding_model() -> SentenceTransformer:
    """
    Load local sentence-transformers model.
    """
    return SentenceTransformer(EMBEDDING_MODEL)


def load_chroma_collection():
    """
    Load the ChromaDB collection created in Milestone 4.
    """
    if not CHROMA_DIR.exists():
        raise FileNotFoundError(
            f"Could not find ChromaDB directory: {CHROMA_DIR}\n\n"
            "Run Milestone 4 first:\n"
            "    python milestone4_embed_retrieve.py --rebuild"
        )

    client = chromadb.PersistentClient(path=str(CHROMA_DIR))

    try:
        collection = client.get_collection(name=COLLECTION_NAME)
    except Exception as exc:
        raise RuntimeError(
            f"Could not load ChromaDB collection: {COLLECTION_NAME}\n\n"
            "Run Milestone 4 first:\n"
            "    python milestone4_embed_retrieve.py --rebuild"
        ) from exc

    return collection


# Load these once so the app does not reload models for every query.
embedding_model = load_embedding_model()
collection = load_chroma_collection()
groq_client = load_groq_client()


# ---------------------------------------------------------------------
# Retrieval
# ---------------------------------------------------------------------

def retrieve_chunks(question: str, top_k: int = DEFAULT_TOP_K) -> List[RetrievedChunk]:
    """
    Retrieve top-k relevant chunks from ChromaDB for a user question.

    Returns source metadata needed for citations.
    """
    question = question.strip()

    if not question:
        return []

    query_embedding = embedding_model.encode(
        [question],
        convert_to_numpy=True,
        normalize_embeddings=True,
    ).tolist()[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    retrieved: List[RetrievedChunk] = []

    for i, (doc, metadata, distance) in enumerate(
        zip(documents, metadatas, distances),
        start=1,
    ):
        retrieved.append(
            RetrievedChunk(
                text=str(doc),
                source_file=str(metadata.get("source_file", "unknown_source")),
                source_id=str(metadata.get("source_id", "unknown_source_id")),
                chunk_index=int(metadata.get("chunk_index", -1)),
                char_count=int(metadata.get("char_count", len(str(doc)))),
                distance=float(distance),
                citation_id=f"S{i}",
            )
        )

    return retrieved


# ---------------------------------------------------------------------
# Grounded generation
# ---------------------------------------------------------------------

def format_context(retrieved_chunks: List[RetrievedChunk]) -> str:
    """
    Format retrieved chunks into a numbered context block for the LLM.

    Each chunk gets a citation id like [S1], [S2], etc.
    """
    context_blocks = []

    for chunk in retrieved_chunks:
        block = f"""
[{chunk.citation_id}]
Source file: {chunk.source_file}
Chunk index: {chunk.chunk_index}
Text:
{chunk.text}
""".strip()

        context_blocks.append(block)

    return "\n\n---\n\n".join(context_blocks)


def build_prompt(question: str, retrieved_chunks: List[RetrievedChunk]) -> str:
    """
    Build a strict grounding prompt.

    The model is not allowed to use outside knowledge.
    """
    context = format_context(retrieved_chunks)

    return f"""
You are a grounded RAG assistant for a project about Sawtelle, Los Angeles food recommendations.

You must follow these rules:
1. Answer using ONLY the retrieved context below.
2. Do NOT use outside knowledge, even if you know the answer.
3. If the retrieved context does not contain enough information to answer, say exactly:
   "{REFUSAL_MESSAGE}"
4. Cite the context chunks you used with bracket citations like [S1] or [S2].
5. Do not cite a source unless the answer is directly supported by that source.
6. Be concise but helpful.

Retrieved context:
{context}

User question:
{question}

Grounded answer:
""".strip()


def should_refuse_from_retrieval(retrieved_chunks: List[RetrievedChunk]) -> bool:
    """
    Refuse early if retrieval looks too weak.

    This prevents the LLM from answering questions that are outside the document set.
    """
    if not retrieved_chunks:
        return True

    best_distance = retrieved_chunks[0].distance

    return best_distance > MAX_DISTANCE_FOR_ANSWER


def generate_grounded_answer(question: str, retrieved_chunks: List[RetrievedChunk]) -> str:
    """
    Generate an answer using Groq, grounded only in retrieved chunks.
    """
    if should_refuse_from_retrieval(retrieved_chunks):
        return REFUSAL_MESSAGE

    prompt = build_prompt(question, retrieved_chunks)

    response = groq_client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You answer questions only from retrieved documents. "
                    "You refuse when the retrieved documents do not contain the answer."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.2,
        max_tokens=700,
    )

    answer = response.choices[0].message.content.strip()

    # Safety check: if the model did not cite sources and did not refuse,
    # add a warning rather than pretending the answer is properly grounded.
    if REFUSAL_MESSAGE not in answer and "[" not in answer:
        answer += (
            "\n\nGrounding warning: The answer did not include citation markers. "
            "Please inspect the retrieved chunks before trusting this response."
        )

    return answer


def get_unique_sources(retrieved_chunks: List[RetrievedChunk]) -> List[str]:
    """
    Get source files used in retrieval.

    This is programmatic source attribution, independent of the LLM.
    """
    seen = set()
    sources = []

    for chunk in retrieved_chunks:
        label = f"{chunk.source_file} — chunk {chunk.chunk_index} — distance {chunk.distance:.4f}"
        if label not in seen:
            seen.add(label)
            sources.append(label)

    return sources


def ask(question: str, top_k: int = DEFAULT_TOP_K) -> Dict[str, Any]:
    """
    End-to-end RAG function:
        question -> retrieve chunks -> generate grounded answer -> return sources
    """
    question = question.strip()

    if not question:
        return {
            "answer": "Please enter a question.",
            "sources": [],
            "retrieved_chunks": [],
        }

    retrieved_chunks = retrieve_chunks(question, top_k=top_k)
    answer = generate_grounded_answer(question, retrieved_chunks)
    sources = get_unique_sources(retrieved_chunks)

    return {
        "answer": answer,
        "sources": sources,
        "retrieved_chunks": retrieved_chunks,
    }


# ---------------------------------------------------------------------
# Gradio interface
# ---------------------------------------------------------------------

def format_sources_for_display(sources: List[str]) -> str:
    """
    Format source list for Gradio.
    """
    if not sources:
        return "No sources retrieved."

    return "\n".join(f"• {source}" for source in sources)


def format_retrieved_chunks_for_display(retrieved_chunks: List[RetrievedChunk]) -> str:
    """
    Display retrieved chunks so the demo can show why an answer is grounded.
    """
    if not retrieved_chunks:
        return "No chunks retrieved."

    blocks = []

    for chunk in retrieved_chunks:
        block = f"""
[{chunk.citation_id}]
Source file: {chunk.source_file}
Chunk index: {chunk.chunk_index}
Distance: {chunk.distance:.4f}
Characters: {chunk.char_count}

{chunk.text}
""".strip()

        blocks.append(block)

    return "\n\n" + ("\n\n" + "-" * 80 + "\n\n").join(blocks)


def handle_query(question: str, top_k: int):
    """
    Gradio wrapper.
    """
    result = ask(question, top_k=top_k)

    answer = result["answer"]
    sources = format_sources_for_display(result["sources"])
    retrieved = format_retrieved_chunks_for_display(result["retrieved_chunks"])

    return answer, sources, retrieved


def build_interface():
    """
    Build Gradio UI.
    """
    with gr.Blocks(title="The Unofficial Guide: Sawtelle Food") as demo:
        gr.Markdown("# The Unofficial Guide: Sawtelle Food Recommendations")
        gr.Markdown(
            "Ask a question about Sawtelle food spots. "
            "The system retrieves relevant document chunks and answers only from those chunks."
        )

        with gr.Row():
            question = gr.Textbox(
                label="Your question",
                placeholder="Example: What are good dessert places in Sawtelle?",
                lines=2,
            )

        with gr.Row():
            top_k = gr.Slider(
                minimum=1,
                maximum=8,
                value=DEFAULT_TOP_K,
                step=1,
                label="Number of chunks to retrieve",
            )

        ask_button = gr.Button("Ask")

        answer = gr.Textbox(
            label="Grounded Answer",
            lines=8,
        )

        sources = gr.Textbox(
            label="Retrieved From",
            lines=6,
        )

        retrieved_chunks = gr.Textbox(
            label="Retrieved Chunks for Inspection",
            lines=16,
        )

        examples = gr.Examples(
            examples=[
                ["What restaurants are recommended for ramen in Sawtelle?", 4],
                ["What are good dessert or sweet snack places in Sawtelle?", 4],
                ["What Sawtelle restaurants are recommended if I do not want ramen, noodles, or sushi?", 4],
                ["What vegetarian-friendly food options are mentioned near Sawtelle or Westwood?", 4],
                ["What is the best pizza place in New York City?", 4],
            ],
            inputs=[question, top_k],
        )

        ask_button.click(
            handle_query,
            inputs=[question, top_k],
            outputs=[answer, sources, retrieved_chunks],
        )

        question.submit(
            handle_query,
            inputs=[question, top_k],
            outputs=[answer, sources, retrieved_chunks],
        )

    return demo


# ---------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------

def run_cli_query(query: str, top_k: int) -> None:
    """
    Run one query from the command line.
    """
    result = ask(query, top_k=top_k)

    print("\n" + "=" * 80)
    print("QUESTION")
    print("=" * 80)
    print(query)

    print("\n" + "=" * 80)
    print("ANSWER")
    print("=" * 80)
    print(result["answer"])

    print("\n" + "=" * 80)
    print("SOURCES")
    print("=" * 80)
    print(format_sources_for_display(result["sources"]))

    print("\n" + "=" * 80)
    print("RETRIEVED CHUNKS")
    print("=" * 80)
    print(format_retrieved_chunks_for_display(result["retrieved_chunks"]))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Milestone 5: Grounded generation and Gradio interface."
    )

    parser.add_argument(
        "--cli",
        type=str,
        default=None,
        help="Run a single command-line query instead of launching Gradio.",
    )

    parser.add_argument(
        "--top-k",
        type=int,
        default=DEFAULT_TOP_K,
        help="Number of chunks to retrieve. Default: 4",
    )

    parser.add_argument(
        "--share",
        action="store_true",
        help="Create a public Gradio share link.",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.top_k <= 0:
        raise ValueError("--top-k must be a positive integer.")

    if args.cli:
        run_cli_query(args.cli, top_k=args.top_k)
        return

    demo = build_interface()
    demo.launch(share=args.share)


if __name__ == "__main__":
    main()
