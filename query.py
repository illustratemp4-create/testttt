import groq
from embedding import embed_chunks, search
from dotenv import load_dotenv
import os
from groq import Groq
load_dotenv()


def query_llm(json_chunks, queries):
    client = Groq(
        api_key=os.environ['GROQ_API_KEY'],
    )

    chunks, embeddings = embed_chunks(json_chunks)

    # LLM prompt to extract important keywords that can be used to query the document for relevant information
    key_prompt = f"""You are an expert legal assistant.
        You are given a set of questions and a document to query to get the answers from. Give your answer as a set of keywords that you would use to query the document using cosine similarity search.
        Separate each set of keywords with a '|'. Do not repeat the questions in the answer, don't give any pretext.

        Question:
        {queries}

        Answer: """
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"{key_prompt}",
            }
        ],
        model="meta-llama/llama-4-scout-17b-16e-instruct",
    )
    key_answers = chat_completion.choices[0].message.content
    key_answers = key_answers.split('|')
    key_answers = [answer.strip() for answer in key_answers if answer]

    # Context extracted using keywords extracted using llm
    context1 = ''
    for query in key_answers:
        top_chunks = search(query, chunks, embeddings)

        context1 += '\n\n'.join(top_chunks)

    # Context extracted using keywords in the original query (only used if number of questions is small
    # to avoid llm rate limits on message size
    context2 = ''
    for query in queries:
        top_chunks = search(query, chunks, embeddings)

        context2 += '\n\n'.join(top_chunks)

    # Prompt for llm batch query
    prompt = f"""You are an expert legal assistant.
    Use the following context to answer the following questions.
    Separate each answer with a '|'. Do not repeat the questions in the answer.
    
    Context:
    {context1 + context2}
    
    Question:
    {queries}
    
    Answer: """

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"{prompt}",
                }
            ],
            model="meta-llama/llama-4-scout-17b-16e-instruct",
        )
        answers = chat_completion.choices[0].message.content
    except groq.APIStatusError:
        # If using both contexts in the prompt is too large for the llm model
        prompt = f"""You are an expert legal assistant.
            Use the following context to answer the following questions.
            Separate each answer with a '|'. Do not repeat the questions in the answer.

            Context:
            {context1}

            Question:
            {queries}

            Answer: """
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"{prompt}",
                }
            ],
            model="meta-llama/llama-4-scout-17b-16e-instruct",
        )
        answers = chat_completion.choices[0].message.content

    # Postprocessing
    answers = answers.split('|')
    answers = [answer.strip() for answer in answers if answer.strip() != ""]
    # LLM seems to send a '-' sometimes, even when prompted not to.
    if answers[0] == '-':
        answers = answers[1:]

    ans = {"answers": answers}

    return ans