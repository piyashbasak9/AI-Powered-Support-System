from pinecone import Pinecone, ServerlessSpec
from django.conf import settings
from shared.constants import EMBEDDING_DIMENSION, DEFAULT_TOP_K
import time

pc = Pinecone(api_key=settings.PINECONE_API_KEY)
index_name = settings.PINECONE_INDEX_NAME

def ensure_index_exists():
    try:
        if index_name not in pc.list_indexes().names():
            pc.create_index(
                name=index_name,
                dimension=EMBEDDING_DIMENSION,
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1")
            )
            while not pc.describe_index(index_name).status.get('ready', False):
                time.sleep(2)
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def search_similar(query_embedding, top_k=DEFAULT_TOP_K):
    index = pc.Index(index_name)
    results = index.query(vector=query_embedding, top_k=top_k, include_metadata=True)
    
    return [{
        "id": match.id,
        "score": match.score,
        "text": match.metadata.get("text", ""),
        "metadata": match.metadata
    } for match in results.matches]