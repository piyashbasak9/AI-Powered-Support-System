import uuid
import time
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import AskQuestionForm
from .models import QueryLog
from .utils.embeddings import get_query_embedding
from .utils.llm import generate_answer
from .utils.vector_store import search_similar, ensure_index_exists
from .utils.file_processor import process_uploaded_file
from .utils.ticket_client import create_ticket

def home(request):
    return render(request, 'user/index.html', {'form': AskQuestionForm()})

@csrf_exempt
def ask_question(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    start_time = time.time()
    form = AskQuestionForm(request.POST, request.FILES)
    
    if not form.is_valid():
        return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    
    query = form.cleaned_data['query']
    file = form.cleaned_data.get('file')
    
    try:
        # Process file if uploaded
        extracted_text = ""
        file_info = None
        if file:
            result = process_uploaded_file(file)
            extracted_text = result["extracted_text"]
            file_info = result["file_info"]
        
        full_text = query + ("\n\n" + extracted_text if extracted_text else "")
        
        # Ensure Pinecone index exists
        ensure_index_exists()
        
        # Search for relevant content
        query_embedding = get_query_embedding(full_text)
        matches = search_similar(query_embedding)
        
        # If no matches, create ticket
        if not matches:
            ticket_id = str(uuid.uuid4())
            create_ticket(ticket_id, query, extracted_text, file_info)
            
            return JsonResponse({
                'status': 'ticket_created',
                'ticket_id': ticket_id,
                'message': 'Support ticket created. You will be contacted shortly.'
            })
        
        # Generate answer from matches
        context = "\n\n".join([m["text"] for m in matches])
        answer = generate_answer(query, context)
        
        # If no answer found, create ticket
        if answer == "NO_INFO":
            ticket_id = str(uuid.uuid4())
            create_ticket(ticket_id, query, extracted_text, file_info)
            
            return JsonResponse({
                'status': 'ticket_created',
                'ticket_id': ticket_id,
                'message': 'Answer not found. Ticket created.'
            })
        
        # Log and return answer
        QueryLog.objects.create(
            query=query[:500],
            response_status="answered"
        )
        
        return JsonResponse({
            'status': 'success',
            'answer': answer,
            'sources': [{'text': m['text'][:200], 'score': m['score']} for m in matches]
        })
        
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    finally:
        # Log timing
        latency = (time.time() - start_time) * 1000
        print(f"Request latency: {latency}ms")