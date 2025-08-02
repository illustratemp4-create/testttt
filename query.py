from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
from dotenv import load_dotenv
import os
from groq import Groq

load_dotenv()


def query_llm(queries):
    pc = Pinecone(api_key=os.environ['PINECONE_API_KEY'])
    index = pc.Index(host=os.environ['PINECONE_HOST'])

    client = Groq(
        api_key=os.environ['GROQ_API_KEY'],
    )

    model = SentenceTransformer('BAAI/bge-base-en-v1.5')

    # queries = [
    #         "What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?",
    #         "What is the waiting period for pre-existing diseases (PED) to be covered?",
    #         "Does this policy cover maternity expenses, and what are the conditions?",
    #         "What is the waiting period for cataract surgery?",
    #         "Are the medical expenses for an organ donor covered under this policy?",
    #         "What is the No Claim Discount (NCD) offered in this policy?",
    #         "Is there a benefit for preventive health check-ups?",
    #         "How does the policy define a 'Hospital'?",
    #         "What is the extent of coverage for AYUSH treatments?",
    #         "Are there any sub-limits on room rent and ICU charges for Plan A?"
    #     ]

    answers = []

    for query in queries:
        query_embed = model.encode(query).tolist()

        res = index.query(vector=query_embed, top_k=5, include_metadata=True, namespace="Insurance")
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
        answers.append(chat_completion.choices[0].message.content)

    # print("ANSWERS:")
    # for i in range(len(answers)):
    #     print(f"\n{i + 1}. {answers[i]}")

    ans = {"answers": answers}

    return ans