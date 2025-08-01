from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
from dotenv import load_dotenv
import os
# from openai import OpenAI
from groq import Groq

load_dotenv()

pc = Pinecone(api_key=os.environ['PINECONE_API_KEY'])
index = pc.Index(host=os.environ['PINECONE_HOST'])

client = Groq(
    api_key=os.environ['GROQ_API_KEY'],
)

# client = OpenAI(
#     api_key=os.environ['GROQ_API_KEY'],
#     base_url="https://api.groq.com/openai/v1"
# )

model = SentenceTransformer('BAAI/bge-base-en-v1.5')

query = "Does this policy cover maternity expenses, and what are the conditions?"

query_embed = model.encode(query).tolist()

res = index.query(vector=query_embed, top_k=5, include_metadata=True, namespace="Arogya")
# print(res)
docs = [match['metadata']['text'] for match in res['matches']]
# print(docs)

context = '\n\n'.join(docs)

prompt = f"""You are an expert legal assistant.
Use the following context to answer the question.
If it's not answerable from the text, say "Not found in document"

Context:
{context}

Question:
{query}

Answer: """

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": f"{prompt}",
        }
    ],
    model="llama-3.3-70b-versatile",
)

print(chat_completion.choices[0].message.content)

# response = client.chat.completions.create(
#     model="llama-3.3-70b-versatile",
#     messages=[{"role": "user", "content": prompt}]
# )
#
# answer = response.choices[0].message.content
# print("Answer:", answer)