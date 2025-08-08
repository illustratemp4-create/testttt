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

        prompt = f"""
        You are an expert insurance policy assistant.

        Use ONLY the information provided in the context below to answer the question accurately and concisely.

        RULES:
        - Do NOT use any external knowledge.
        - If the answer is not clearly stated in the context, respond with: "Not found in document".
        - Quote exact limits or durations when available.
        - Do NOT include any escape characters, backslashes, or formatting artifacts.
        - Avoid overly long answers — keep it short and factual (ideally under 3 sentences).
        - Do not explain the clause numbers or legal citations unless necessary for clarity.
        - Use a clear, formal, and factual tone (avoid legalese unless quoting a definition).
        - Remove any unnecessary slash-n's and slashes that are not part of the answer.

        Context:
        {context}

        Question:
        {query}

        Answer:
        """

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"{prompt}",
                }
            ],
            model="meta-llama/llama-4-scout-17b-16e-instruct",
        )
        answers.append(chat_completion.choices[0].message.content)
    cleaned_answers = [ans.replace('\n', ' ').replace('\r', ' ').strip() for ans in answers]
    ans = {"answers": cleaned_answers}

    return ans