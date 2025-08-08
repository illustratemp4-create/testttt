from pinecone_db import embed_chunks, search
from dotenv import load_dotenv
import os
from groq import Groq

load_dotenv()


def query_llm(json_chunks, queries):
    client = Groq(
        api_key=os.environ['GROQ_API_KEY'],
    )

    chunks, embeddings = embed_chunks(json_chunks)

    answers = []

    for query in queries:
        top_chunks = search(query, chunks, embeddings)

        context = '\n\n'.join(top_chunks)

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
        answers.append(chat_completion.choices[0].message.content)

    ans = {"answers": answers}

    return ans