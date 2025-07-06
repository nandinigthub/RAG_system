from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List
from backend.controller.vector_db import get_vectorstore
import uuid
from langchain_core.documents import Document

from langchain_text_splitters import (
    TokenTextSplitter,
)


def GetTextSplitter(chunk_size: int = 1536, chunk_overlap: int = 100):
    return TokenTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

def chunk_text(text: str, chunk_size=500, chunk_overlap=50):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return [{"type": "text", "content": chunk} for chunk in splitter.split_text(text)]

def chunk_tables(tables: list[dict]) -> list[dict]:
    chunks = []
    for table in tables:
        rows = table["data"]
        page = table["page"]
        if not rows:
            continue
        header = " | ".join(rows[0])
        separator = " | ".join(["---"] * len(rows[0]))
        body = "\n".join(" | ".join(row) for row in rows[1:])
        content = f"Table from page {page}\n\n{header}\n{separator}\n{body}"
        chunks.append({"type": "table", "content": content, "page": page})
    return chunks

def prepare_chunks(text: str, tables=[]) -> list[dict]:
    return chunk_text(text) + chunk_tables(tables)


def embed_chunks(chunks: List[dict]):
    text = " ".join(chunk["content"] for chunk in chunks)
    
    text_splitter = GetTextSplitter()
    documents = text_splitter.split_documents([
        Document(page_content=text, metadata={"doc_id": str(uuid.uuid4())})
    ])
    return get_vectorstore().add_documents(documents)
