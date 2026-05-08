import google.generativeai as genai
from django.conf import settings
from shared.constants import EMBEDDING_MODEL, EMBEDDING_DIMENSION

genai.configure(api_key=settings.GEMINI_API_KEY)

def get_embedding(text, task_type="RETRIEVAL_DOCUMENT"):
    result = genai.embed_content(
        model=EMBEDDING_MODEL,
        content=text,
        task_type=task_type,
    )
    return result["embedding"]

def get_query_embedding(query):
    return get_embedding(query, task_type="RETRIEVAL_QUERY")