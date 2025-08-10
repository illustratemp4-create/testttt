import fitz
import requests
from io import BytesIO
import re
from collections import Counter


def download_and_extract(url):
    response = requests.get(url)
    pdf = fitz.open(stream=BytesIO(response.content), filetype="pdf")
    # full_text = ""
    # for page in pdf:
    #     full_text += page.get_text()
    # # with open('files.txt', 'a', encoding='utf-8') as file:
    # #     file.write('New pdf here: \n' + full_text + '\n')
    # # print(full_text)
    # return full_text
    pages_text = []
    all_lines = []

    # Collect raw text per page
    for page in pdf:
        text = page.get_text("text")
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        pages_text.append(lines)
        all_lines.extend(lines)

    # Detect common lines (likely headers/footers)
    line_counts = Counter(all_lines)
    repeated_lines = {line for line, count in line_counts.items() if count > 1}

    cleaned_pages = []
    for lines in pages_text:
        cleaned_lines = [line for line in lines if line not in repeated_lines]
        cleaned_pages.append(" ".join(cleaned_lines))

    # Join pages into one clean string
    full_text = "\n\n".join(cleaned_pages)

    # Optional: normalize spaces & remove page numbers
    full_text = re.sub(r"\bPage\s*\d+\b", "", full_text, flags=re.IGNORECASE)
    full_text = re.sub(r"\s+", " ", full_text).strip()

    return full_text


def chunk_text(text, chunk_size=500, overlap=50):
    sentences = re.split(r'(?<=[.?!])\s+', text)
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) + 1 > chunk_size:
            chunks.append(current_chunk.strip())
            # Start new chunk with overlap from the end of the last chunk
            if overlap > 0 and chunks[-1]:
                overlap_text = chunks[-1][-overlap:]
                current_chunk = overlap_text + " " + sentence
            else:
                current_chunk = sentence
        else:
            current_chunk += " " + sentence

    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    return chunks