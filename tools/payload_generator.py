"""Generate API-ready document and chunk payloads from Cohere embeddings.

This script strictly requires the Cohere V2 JSON response to include:
  {
    "embeddings": {"float": [[...], ...]},
    "texts": ["text1", "text2", ...]
  }

If the response doesn't match that shape, the script will not write any payloads.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import uuid
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class ChunkPayload:
    text: str
    embedding: List[float]
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "embedding": self.embedding,
            "metadata": self.metadata,
        }


@dataclass
class DocumentPayload:
    title: str
    author: Optional[str]
    custom_fields: Dict[str, Any]
    chunks: List[ChunkPayload]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "metadata": {
                "title": self.title,
                "author": self.author,
                "custom_fields": self.custom_fields,
            },
            "chunks": [c.to_dict() for c in self.chunks],
        }


def _load_texts_from_file(path: str) -> List[str]:
    with open(path, "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh.readlines() if line.strip()]


def _write_json(path: str, data: Any) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)


def call_cohere_and_build(
    texts: List[str],
    api_key: str,
    title: str,
    source: str,
    out_dir: str,
    doc_name: str,
    author: Optional[str] = None,
) -> None:
    try:
        import cohere
    except Exception as exc:  # pragma: no cover - runtime dependency
        print("The 'cohere' package is required. Install with: pip install cohere")
        raise exc

    client = cohere.ClientV2(api_key=api_key)

    MAX_INPUTS = 96
    if len(texts) > MAX_INPUTS:
        print(
            f"WARNING: too many texts provided ({len(texts)}). Cohere embed supports a maximum of {MAX_INPUTS} inputs per request."
        )
        print(
            "No payloads written. Please reduce the number of texts or split into batches."
        )
        return

    text_inputs = [{"content": [{"type": "text", "text": t}]} for t in texts]
    resp = client.embed(
        inputs=text_inputs,
        model="embed-v4.0",
        input_type="search_document",
        embedding_types=["float"],
        output_dimension=256,
    )
    embs = resp.embeddings.float_

    if not embs or len(embs) != len(texts):
        print("Cohere response missing embeddings or text count mismatch.")
        print("No payloads written.")
        return

    all_pairs = [
        {"text": texts[i], "embedding": list(map(float, embs[i]))}
        for i in range(len(embs))
    ]

    chunks: List[ChunkPayload] = []
    for p in all_pairs:
        chunks.append(
            ChunkPayload(
                text=p["text"],
                embedding=p["embedding"],
                metadata={"source": source, "page_number": None, "custom_fields": {}},
            )
        )

    doc = DocumentPayload(title=title, author=author, custom_fields={}, chunks=chunks)

    run_id = uuid.uuid4().hex[:8]
    run_dir = os.path.join(out_dir, f"run_{run_id}")
    os.makedirs(run_dir, exist_ok=True)

    out_doc = os.path.join(run_dir, doc_name)
    _write_json(out_doc, doc.to_dict())
    print(f"Wrote document payload to {out_doc}")

    for idx, c in enumerate(chunks):
        out_chunk = os.path.join(run_dir, f"chunk_{idx}.json")
        _write_json(out_chunk, c.to_dict())
    print(f"Wrote {len(chunks)} chunk payloads to {run_dir}")


def main():
    parser = argparse.ArgumentParser(description="Call Cohere and produce API payloads")
    parser.add_argument("--texts-file", help="Path to newline-delimited texts file")
    parser.add_argument(
        "--text", action="append", help="Text to embed (can be repeated)"
    )
    parser.add_argument("--out-dir", default="test_data", help="Output directory")
    parser.add_argument(
        "--doc-name", default="doc_payload.json", help="Document output file name"
    )
    parser.add_argument("--title", default="My Amazing Document", help="Document title")
    parser.add_argument("--author", default="Vinícius Albano", help="Document author")
    parser.add_argument("--source", default="Cohere", help="Chunk metadata.source")
    args = parser.parse_args()

    texts: List[str] = []
    if args.texts_file:
        texts.extend(_load_texts_from_file(args.texts_file))
    if args.text:
        texts.extend(args.text)
    if not texts:
        print("No texts provided. Use --texts-file or --text.")
        sys.exit(1)

    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        print("COHERE_API_KEY environment variable is required. Set it and retry.")
        sys.exit(1)

    call_cohere_and_build(
        texts=texts,
        api_key=api_key,
        title=args.title,
        author=args.author,
        source=args.source,
        out_dir=args.out_dir,
        doc_name=args.doc_name,
    )


if __name__ == "__main__":
    main()
