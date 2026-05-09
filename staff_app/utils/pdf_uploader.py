import io
import pdfplumber
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pinecone import Pinecone
from django.conf import settings
from shared.constants import DEFAULT_CHUNK_SIZE, DEFAULT_CHUNK_OVERLAP

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=DEFAULT_CHUNK_SIZE,
    chunk_overlap=DEFAULT_CHUNK_OVERLAP,
)

def extract_text_from_pdf(file_bytes):
    text = ""
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()

def chunk_text(text):
    if not text:
        return []
    return text_splitter.split_text(text)

def get_embedding(text):
    from sentence_transformers import SentenceTransformer
    from shared.constants import EMBEDDING_MODEL
    
    model = SentenceTransformer(EMBEDDING_MODEL)
    return model.encode(text).tolist()

def process_pdf_and_upload(file_bytes, filename):
    # Extract text
    text = extract_text_from_pdf(file_bytes)
    if not text:
        return {"status": "error", "message": "No text extracted", "chunks": 0}
    
    # Chunk text
    chunks = chunk_text(text)
    if not chunks:
        return {"status": "error", "message": "No chunks created", "chunks": 0}
    
    # Generate embeddings and upload to Pinecone
    try:
        pc = Pinecone(api_key=settings.PINECONE_API_KEY)
        index = pc.Index(settings.PINECONE_INDEX_NAME)
        
        vectors = []
        for i, chunk in enumerate(chunks):
            embedding = get_embedding(chunk)
            vectors.append({
                "id": f"{filename}_{i}",
                "values": embedding,
                "metadata": {
                    "text": chunk,
                    "source": filename,
                    "chunk_index": i
                }
            })
        
        # Upload in batches
        for i in range(0, len(vectors), 100):
            index.upsert(vectors=vectors[i:i+100])
        
        return {"status": "success", "message": f"Uploaded {len(chunks)} chunks", "chunks": len(chunks)}
        
    except Exception as e:
        return {"status": "error", "message": str(e), "chunks": 0}