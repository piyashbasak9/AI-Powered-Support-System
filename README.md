# AI-Powered Support System (RAG)

A Django-based support system that combines retrieval-augmented generation with Pinecone vector search and Groq/OpenAI-powered language generation.

## Features

- **User-facing question portal**: Users can ask questions and upload documents for context
- **Document ingestion**: PDF text extraction via `pdfplumber`
- **Semantic search**: Pinecone vector search using embeddings from `sentence-transformers`
- **AI answer generation**: Context-aware response generation via Groq/OpenAI chat completions
- **Automated ticket creation**: Creates support tickets when answers are not found
- **Staff dashboard**: Staff can view uploaded documents, pending tickets, and resolved tickets
- **Ticket resolution**: Staff can answer and resolve pending support tickets

## Requirements

- Python 3.10+
- SQLite (included by default with Django)
- Pinecone account and API key
- Groq/OpenAI API key

## Setup

1. Clone the repository
   ```bash
   git clone https://github.com/piyashbasak9/AI-Powered-Support-System.git
   cd RAG_Support_system
   ```

2. Create and activate a virtual environment
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install Python dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file at the project root with the following values
   ```env
   DJANGO_SECRET_KEY=your_secret_key
   PINECONE_API_KEY=your_pinecone_api_key
   PINECONE_ENVIRONMENT=gcp-starter
   PINECONE_INDEX_NAME=rag-support-index-v3
   GROQ_API_KEY=your_groq_api_key
   STAFF_SERVER_URL=http://localhost:8000/staff/api/create-ticket/
   ```

5. Run database migrations
   ```bash
   python manage.py migrate
   ```

6. Create a superuser (optional)
   ```bash
   python manage.py createsuperuser
   ```

7. Start the development server
   ```bash
   python manage.py runserver
   ```

## Usage

- **User portal**: `http://localhost:8000/`
- **Staff login**: `http://localhost:8000/staff/login/`
- **Django admin**: `http://localhost:8000/admin/`

> Note: The staff login view will automatically create a default staff user with username `staff` and password `staff123` if one does not already exist.

## How it works

1. A user submits a query and optionally uploads a PDF.
2. The system extracts text from the uploaded file and combines it with the query.
3. It generates an embedding and searches Pinecone for relevant content.
4. If matching context is found, it calls the Groq/OpenAI chat completion API to generate an answer.
5. If no answer is found, a support ticket is created for staff review.

## Project Structure

```
RAG_Support_system/
├── core/              # Django project configuration
├── staff_app/         # Staff dashboard, ticket management, PDF uploads
│   ├── models.py
│   ├── views.py
│   └── utils/pdf_uploader.py
├── user_app/          # User-facing question portal and retrieval logic
│   ├── models.py
│   ├── views.py
│   └── utils/
│       ├── embeddings.py
│       ├── file_processor.py
│       ├── llm.py
│       └── vector_store.py
├── shared/            # Shared constants and configuration helpers
├── templates/         # Django HTML templates
├── media/             # Uploaded files storage
├── db.sqlite3         # SQLite database file
├── manage.py
└── requirements.txt
```

## Configuration

- `PINECONE_API_KEY`: Pinecone API key for vector index operations
- `PINECONE_ENVIRONMENT`: Pinecone environment (default: `gcp-starter`)
- `PINECONE_INDEX_NAME`: Pinecone index name
- `GROQ_API_KEY`: Groq/OpenAI API key for text generation
- `DJANGO_SECRET_KEY`: Django secret key
- `STAFF_SERVER_URL`: Endpoint used by the app to create tickets

## Contributing

1. Fork the repository
2. Create a new branch
3. Make changes and test locally
4. Open a pull request

## License

MIT License
</content>
<parameter name="filePath">/mnt/ce64fe46-49c4-493a-9d1f-1115b051b230/RAG_Support_system/README.md