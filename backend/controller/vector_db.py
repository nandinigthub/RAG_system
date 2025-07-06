from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct
from langchain_community.vectorstores import Qdrant as LangQdrant
from langchain_community.embeddings import HuggingFaceEmbeddings
import os

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", None)

client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
)

COLLECTION_NAME = "pdf_chunks"
DIMENSION = 768


def init_qdrant():
    collections = client.get_collections().collections
    if COLLECTION_NAME not in [col.name for col in collections]:
        client.recreate_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=768, distance=Distance.COSINE),
        )


def upsert_document(document_id: str, vector: list[float], metadata: dict):
    if isinstance(vector, list) and isinstance(vector[0], list):
        vector = vector[0]
    client.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            PointStruct(
                id=document_id,
                vector=vector,
                payload=metadata,
            )
        ],
    )


def get_vectorstore():
    embedder = HuggingFaceEmbeddings(model_name="all-mpnet-base-v2")
    return LangQdrant(
        client=client,
        collection_name=COLLECTION_NAME,
        embeddings=embedder,
    )

def search_similar(query: str, top_k: int = 5):
    print(query)
    results = get_vectorstore().similarity_search(
        query=query,
        k=top_k
    )
    return results