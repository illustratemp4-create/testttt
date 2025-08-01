from extract_chunk_support import download_and_extract, chunk_text
import json
from dotenv import load_dotenv
import os

load_dotenv()

x = download_and_extract(os.environ['AROGYA_FILE_LINK'])
chunks = chunk_text(x)
d = {i: chunks[i] for i in range(len(chunks))}
json_chunks = []
for key, item in d.items():
    temp = {
        'file_name': 'Arogya',
        'chunk_id': key,
        'text': item,
    }
    json_chunks.append(temp)
with open('arogya_parse_chunks.json', 'w', encoding='utf-8') as file:
    json.dump(json_chunks, file)