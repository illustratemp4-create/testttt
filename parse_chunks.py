from extract_chunk_support import download_and_extract, chunk_text
import json


def parse_chunk(url):
    x = download_and_extract(url)
    chunks = chunk_text(x)
    d = {i: chunks[i] for i in range(len(chunks))}
    json_chunks = []
    for key, item in d.items():
        temp = {
            'file_name': 'Insurance',
            'chunk_id': key,
            'text': item,
        }
        json_chunks.append(temp)

    ans = json.dumps(json_chunks)
    return ans