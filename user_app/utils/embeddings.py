from sentence_transformers import SentenceTransformer
from shared.constants import EMBEDDING_MODEL

model = SentenceTransformer(EMBEDDING_MODEL)

def get_embedding(text, task_type="RETRIEVAL_DOCUMENT"):
    # For simplicity, ignore task_type as sentence-transformers doesn't have that
    return model.encode(text).tolist()

def get_query_embedding(query):
    return get_embedding(query, task_type="RETRIEVAL_QUERY")