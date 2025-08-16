# main.py
import os
from fastapi import FastAPI, Header, HTTPException, Body, File, UploadFile, Form
import json
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


@app.post("/hackrx/run-file")
async def run_file(
    file: UploadFile = File(...),
    questions_json: str = Form(...),
    header: str = Header(None, alias="Authorization"),
):
    # Authorization check
    auth = os.environ["HACKRX_API_KEY"]
    if not header or header != f"{auth}":
        raise HTTPException(status_code=401, detail="UNAUTHORIZED")

    # Basic validation
    if file.content_type not in ("application/pdf",):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    # Read the uploaded PDF into memory (bytes)
    pdf_bytes = await file.read()

    # Convert questions JSON string -> list[str]
    try:
        questions = json.loads(questions_json)
        if not isinstance(questions, list) or not all(isinstance(x, str) for x in questions):
            raise ValueError
    except Exception:
        raise HTTPException(status_code=400, detail="questions_json must be a JSON array of strings")

    # Let your existing parser handle bytes/text
    # (see small tweak to parse_chunk below)
    chunks = parse_chunk(pdf_bytes)

    return query_llm(chunks, questions)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)