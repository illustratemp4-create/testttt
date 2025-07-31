import fitz
import requests
from io import BytesIO


def download_and_extract(url):
    response = requests.get(url)
    pdf = fitz.open(stream=BytesIO(response.content), filetype="pdf")
    full_text = ""
    for page in pdf:
        full_text += page.get_text()
    return full_text


def chunk_text(text, chunk_size=500):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]