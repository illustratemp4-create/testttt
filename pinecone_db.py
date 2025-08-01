import json
import uuid
from pinecone import Pinecone
from tqdm import tqdm
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import os

load_dotenv()

pc = Pinecone(api_key=os.environ['PINECONE_API_KEY'])
# print(pc.list_indexes())
index = pc.Index(host=os.environ['PINECONE_HOST'])

# index.delete(delete_all=True, namespace='Bajaj')

# for ids in index.list(namespace='Bajaj'):
#     print(ids)

with open('arogya_parse_chunks.json', 'r', encoding='utf-8') as file:
    chunks = json.load(file)

model = SentenceTransformer('BAAI/bge-base-en-v1.5')

batch = []
for chunk in tqdm(chunks):
    vector = model.encode(chunk['text']).tolist()
    vector_id = str(uuid.uuid4())

    metadata = {
        'text': chunk['text'],
        'file': chunk['file_name'],
        'chunk_id': chunk['chunk_id']
    }

    batch.append((vector_id, vector, metadata))

    if len(batch) == 100:
        index.upsert(vectors=batch, namespace='Arogya')
        batch = []

if batch:
    index.upsert(vectors=batch, namespace='Arogya')

print(f'Uploaded {len(chunks)} chunks to pinecone')