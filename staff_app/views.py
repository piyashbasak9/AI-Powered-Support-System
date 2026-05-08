import uuid
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Ticket
from .utils.pdf_uploader import process_pdf_and_upload

def staff_login(request):
    # Create default staff user if not exists
    if not User.objects.filter(username='staff').exists():
        User.objects.create_user(username='staff', password='staff123', is_staff=True)
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('staff_dashboard')
        else:
            return render(request, 'staff/login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'staff/login.html')

@login_required
def dashboard(request):
    tickets = Ticket.objects.filter(status='pending').order_by('-created_at')
    resolved = Ticket.objects.filter(status='resolved').count()
    pending = Ticket.objects.filter(status='pending').count()
    
    return render(request, 'staff/dashboard.html', {
        'tickets': tickets,
        'pending_count': pending,
        'resolved_count': resolved,
        'total_count': pending + resolved
    })

@login_required
def resolve_ticket(request, ticket_id):
    if request.method == 'POST':
        answer = request.POST.get('answer')
        ticket = Ticket.objects.get(ticket_id=ticket_id)
        ticket.status = 'resolved'
        ticket.answer = answer
        ticket.resolved_at = timezone.now()
        ticket.resolved_by = request.user.username
        ticket.save()
    
    return redirect('staff_dashboard')

@login_required
def upload_pdf(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        content = file.read()
        
        result = process_pdf_and_upload(content, file.name)
        
        return JsonResponse(result)
    
    return JsonResponse({'error': 'No file provided'}, status=400)

@csrf_exempt
def api_create_ticket(request):
    if request.method == 'POST':
        ticket = Ticket.objects.create(
            ticket_id=request.POST.get('ticket_id'),
            query=request.POST.get('query'),
            extracted_text=request.POST.get('extracted_text', ''),
            file_info=request.POST.get('file_info')
        )
        return JsonResponse({'status': 'created', 'ticket_id': ticket.ticket_id}, status=201)
    return JsonResponse({'error': 'Method not allowed'}, status=405)