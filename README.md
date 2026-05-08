# AI-Powered Support System (RAG)

A Django-based RAG (Retrieval-Augmented Generation) support system that uses Pinecone for vector storage and Google Gemini for AI-powered responses.

## Features

- **User Interface**: Web interface for users to ask questions
- **Staff Dashboard**: Admin interface for managing support tickets and uploading documents
- **Document Processing**: PDF upload and text extraction
- **Vector Search**: Semantic search using embeddings
- **AI Responses**: Context-aware answers using Gemini AI
- **Ticket System**: Automated ticket creation for unresolved queries

## Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/piyashbasak9/AI-Powered-Support-System.git
   cd AI-Powered-Support-System
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment variables**
   Create a `.env` file with:
   ```
   PINECONE_API_KEY=your_pinecone_api_key
   GEMINI_API_KEY=your_gemini_api_key
   DJANGO_SECRET_KEY=your_secret_key
   ```

5. **Database setup**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the server**
   ```bash
   python manage.py runserver
   ```

## Usage

- **User Portal**: http://localhost:8000/ - Ask questions
- **Staff Login**: http://localhost:8000/staff/login/ - Admin access
- **Admin Panel**: http://localhost:8000/admin/ - Django admin

## API Keys Required

- **Pinecone**: For vector database storage
- **Google Gemini**: For AI text generation and embeddings

## Architecture

- **Frontend**: Django templates with Bootstrap
- **Backend**: Django REST framework
- **Vector DB**: Pinecone
- **AI Models**: Google Gemini 2.0 Flash
- **Embeddings**: Gemini Embedding-001 (3072 dimensions)

## File Structure

```
├── core/                 # Django settings
├── user_app/            # User-facing application
│   ├── utils/
│   │   ├── llm.py       # AI response generation
│   │   ├── embeddings.py # Text embeddings
│   │   ├── vector_store.py # Pinecone operations
│   │   └── file_processor.py # Document processing
├── staff_app/           # Staff management
│   └── utils/
│       └── pdf_uploader.py # PDF processing
├── templates/           # HTML templates
└── static/              # Static files
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License</content>
<parameter name="filePath">/mnt/ce64fe46-49c4-493a-9d1f-1115b051b230/RAG_Support_system/README.md