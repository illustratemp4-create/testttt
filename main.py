#Without frontend
import os
from fastapi import FastAPI, Header, HTTPException, Body
from parse_chunks import parse_chunk
from query import query_llm
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List
import uvicorn

load_dotenv()

app = FastAPI()


class RequestData(BaseModel):
    documents: str
    questions: List[str]


@app.get("/")
async def home():
    # Sample page
    return {'hello': 'world'}


@app.post("/hackrx/run")
async def root(request_data: RequestData = Body(...),
               header: str = Header(None, alias="Authorization")
               ):
    # Authorization check
    auth = os.environ['HACKRX_API_KEY']
    if not header or header != f"{auth}":
        raise HTTPException(status_code=401, detail="UNAUTHORIZED")

    # Chunking
    chunks = parse_chunk(request_data.documents)

    # Querying
    queries = request_data.questions
    return query_llm(chunks, queries)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)