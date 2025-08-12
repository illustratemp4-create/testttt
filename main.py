# main.py
import os
from fastapi import FastAPI, Header, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List
import uvicorn

from parse_chunks import parse_chunk
from query import query_llm

load_dotenv()

app = FastAPI()

# Allow your HTML/JS to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # in prod, set your domain(s)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve the /static path and an index.html at /
app.mount("/static", StaticFiles(directory="public"), name="static")


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

    chunks = parse_chunk(request_data.documents)  # expects a PDF URL or text (see note below)
    return query_llm(chunks, request_data.questions)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)