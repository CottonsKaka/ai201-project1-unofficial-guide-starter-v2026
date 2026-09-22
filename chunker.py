"""
Stage 2 of the pipeline: splitting documents into chunks.

⚠️ THIS IS THE FILE YOU CHANGE IN MILESTONE 3.

`split_documents` below is deliberately plain. It cuts every document into
fixed-size pieces with a fixed overlap and pays no attention to where sentences
or paragraphs end. It works, and it is not good.

On a corpus of short posts it may not cut anything at all: `campus_life` comes
out as 88 documents and 88 chunks, because almost nothing in it reaches 800
characters. That is the baseline, not a bug — Milestone 3 is where you decide
whether one post should stay one chunk.

Your job in Milestone 3 is to replace the *body* of `split_documents` with a
strategy that fits the documents you actually read in Milestone 1. Keep the
name and the shape of what it returns — the rest of the pipeline calls it, and
your README has to name the function that produced your chunks.

If you get stuck for 30 minutes, `fallback_split` is the original. Switch back
to it, write down what you saw, and move on. That's a real observation about
your pipeline, not giving up.
"""

import re
from dataclasses import dataclass

import config
from ingest import Document


@dataclass
class Chunk:
    """One piece of one document."""

    text: str
    source: str        # which file it came from
    index: int         # which chunk within that file, starting at 0
    produced_by: str   # the function that made it — cite this in your README

    @property
    def label(self) -> str:
        return f"{self.source}#{self.index}"


def fallback_split(
    documents: list[Document],
    chunk_size: int | None = None,
    overlap: int | None = None,
) -> list[Chunk]:
    """
    The starter's original chunker. Fixed-size character windows with overlap.

    Keep this function. Milestone 3's stop rule points back at it, and having
    something to compare your own strategy against is useful in unit 2.
    """
    chunk_size = chunk_size or config.CHUNK_SIZE
    overlap = overlap or config.CHUNK_OVERLAP

    if overlap >= chunk_size:
        raise ValueError("overlap has to be smaller than chunk_size")

    chunks: list[Chunk] = []
    for doc in documents:
        start = 0
        index = 0
        while start < len(doc.text):
            piece = doc.text[start : start + chunk_size].strip()
            if piece:
                chunks.append(
                    Chunk(
                        text=piece,
                        source=doc.source,
                        index=index,
                        produced_by="chunker.py::fallback_split",
                    )
                )
                index += 1
            start += chunk_size - overlap

    return chunks


def _title_and_body(text: str) -> tuple[str, str]:
    """
    Every document in campus_life opens with a title line, then a blank line,
    then the post itself — "Laundry in Aldridge Hall", "On the printing quota".
    That line is the only place the building or the topic is named, so it has
    to travel with every chunk cut out of the document.
    """
    lines = text.split("\n")
    title = lines[0].strip()
    body = "\n".join(lines[1:]).strip()
    return title, body


def _paragraphs(body: str) -> list[str]:
    """Split on blank lines. ingest.clean_text has already normalised these."""
    return [p.strip() for p in re.split(r"\n\s*\n", body) if p.strip()]


def _merge_short(paragraphs: list[str], minimum: int) -> list[str]:
    """
    Fold anything under `minimum` characters into its neighbour.

    A one-line paragraph on its own embeds badly — it's the fragment problem
    the brief warns about, arrived at from the other direction.
    """
    merged: list[str] = []
    for para in paragraphs:
        if merged and len(merged[-1]) < minimum:
            merged[-1] = f"{merged[-1]}\n\n{para}"
        else:
            merged.append(para)

    # A short final paragraph has no successor to merge forward into.
    if len(merged) > 1 and len(merged[-1]) < minimum:
        tail = merged.pop()
        merged[-1] = f"{merged[-1]}\n\n{tail}"

    return merged


def _split_long(paragraph: str, ceiling: int) -> list[str]:
    """
    Only fires on a paragraph longer than the ceiling. Cuts between sentences
    so no chunk ends mid-thought — the thing the starter's fixed window did.
    """
    if len(paragraph) <= ceiling:
        return [paragraph]

    pieces: list[str] = []
    current = ""
    for sentence in re.split(r"(?<=[.!?])\s+", paragraph):
        if current and len(current) + 1 + len(sentence) > ceiling:
            pieces.append(current)
            current = sentence
        else:
            current = f"{current} {sentence}".strip()
    if current:
        pieces.append(current)

    return pieces


def split_documents(documents: list[Document]) -> list[Chunk]:
    """
    Paragraph-boundary chunking with the document title carried into every chunk.

    Why this and not a character window: campus_life posts average about 317
    characters, so an 800-character window never cut anything and one post was
    one chunk. That buries a question. dining_kestrel_commons.txt is wait times
    in its first paragraph and opening hours in its second; health_center.txt
    is walk-in hours then counselling. Ask about counselling and the old chunker
    handed back a chunk that was half about something else.

    Why the title is prepended: paragraph two of housing_aldridge_hall_laundry.txt
    reads "Best time to do laundry here is Tuesday or Wednesday morning." On its
    own, "here" names nothing. The building is in the title line. Splitting on
    paragraphs without carrying the title just trades a noise problem for a
    fragment problem.

    Overlap is 0 (config.CHUNK_OVERLAP). Overlap exists to repair thoughts cut
    in half by an arbitrary boundary; a blank line is not arbitrary, and the
    title header already supplies the shared context.
    """
    ceiling = config.CHUNK_SIZE
    minimum = config.MIN_CHUNK_CHARS

    chunks: list[Chunk] = []
    for doc in documents:
        title, body = _title_and_body(doc.text)

        paragraphs = _paragraphs(body)
        if not paragraphs:
            # Title-only document: the title is the whole content.
            pieces = [title] if title else []
            prepend_title = False
        else:
            pieces = []
            for para in _merge_short(paragraphs, minimum):
                pieces.extend(_split_long(para, ceiling))
            prepend_title = bool(title)

        for index, piece in enumerate(pieces):
            text = f"{title}\n\n{piece}" if prepend_title else piece
            chunks.append(
                Chunk(
                    text=text,
                    source=doc.source,
                    index=index,
                    produced_by="chunker.py::split_documents",
                )
            )

    return chunks


def describe(chunks: list[Chunk]) -> str:
    """A one-line summary, printed after indexing."""
    if not chunks:
        return "0 chunks"
    lengths = [len(c.text) for c in chunks]
    return (
        f"{len(chunks)} chunks, "
        f"{sum(lengths) // len(lengths)} characters on average "
        f"(shortest {min(lengths)}, longest {max(lengths)}), "
        f"produced by {chunks[0].produced_by}"
    )


if __name__ == "__main__":
    from ingest import load_documents

    chunks = split_documents(load_documents())
    print(describe(chunks))
