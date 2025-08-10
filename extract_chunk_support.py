import fitz
import requests
from io import BytesIO
import re


def download_and_extract(url):
    response = requests.get(url)
    pdf = fitz.open(stream=BytesIO(response.content), filetype="pdf")
    full_text = ""
    for page in pdf:
        full_text += page.get_text()
    # with open('files.txt', 'a', encoding='utf-8') as file:
    #     file.write('New pdf here: \n' + full_text + '\n')
    # print(full_text)
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