import fitz  # PyMuPDF
import requests
from io import BytesIO
import re
from collections import Counter
from typing import Union

def _extract_pdf_text_from_bytes(pdf_bytes: bytes) -> str:
    """Extract text from a PDF given raw bytes, with de-dup of repeated lines."""
    pdf = fitz.open(stream=BytesIO(pdf_bytes), filetype="pdf")
    pages_text = []
    all_lines = []

    # Collect raw text per page
    for page in pdf:
        text = page.get_text("text")
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        pages_text.append(lines)
        all_lines.extend(lines)

    # Detect common lines (avoid boilerplate repeating across pages)
    line_counts = Counter(all_lines)
    repeated_lines = {line for line, count in line_counts.items() if count > 1}

    cleaned_pages = []
    for lines in pages_text:
        cleaned_lines = [line for line in lines if line not in repeated_lines]
        cleaned_pages.append(" ".join(cleaned_lines))

    full_text = "\n\n".join(cleaned_pages)

    # Normalize
    full_text = re.sub(r"\bPage\s*\d+\b", "", full_text, flags=re.IGNORECASE)
    full_text = re.sub(r"\s+", " ", full_text).strip()

    return full_text


def extract_text(source: Union[str, bytes]) -> str:
    """
    Polymorphic extractor:
      - bytes -> treat as PDF bytes
      - str starting with http(s) -> download URL as PDF and extract
      - other str -> treat as plain text (already-extracted)
    """
    if isinstance(source, bytes):
        return _extract_pdf_text_from_bytes(source)

    if isinstance(source, str):
        s = source.strip()
        # URL to a PDF
        if s.lower().startswith(("http://", "https://")):
            resp = requests.get(s)
            resp.raise_for_status()
            return _extract_pdf_text_from_bytes(resp.content)

        # Fall back to plain text (already extracted)
        return s

    raise TypeError("Unsupported source type for extract_text; expected str or bytes.")


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50):
    sentences = re.split(r"(?<=[.?!])\s+", text)
    chunks = []
    current_chunk = ""

    # performs chunking with ~10% overlaps (controlled by 'overlap' param)
    for sentence in sentences:
        if len(current_chunk) + len(sentence) + 1 > chunk_size:
            chunks.append(current_chunk.strip())
            if overlap > 0 and chunks[-1]:
                overlap_text = chunks[-1][-overlap:]
                current_chunk = (overlap_text + " " + sentence).strip()
            else:
                current_chunk = sentence
        else:
            current_chunk = (current_chunk + " " + sentence).strip()

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks
