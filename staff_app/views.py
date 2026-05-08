import uuid
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.files.base import ContentFile
from .models import Ticket, UploadedFile
from .utils.pdf_uploader import process_pdf_and_upload


def staff_login(request):
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
            return render(request, 'staff/login.html', {"error": "Invalid credentials"})

    return render(request, 'staff/login.html')


@login_required
def dashboard(request):
    uploaded_files = UploadedFile.objects.all().order_by('-uploaded_at')
    pending = Ticket.objects.filter(status='pending').count()
    resolved = Ticket.objects.filter(status='resolved').count()

    return render(request, 'staff/dashboard.html', {
        'files': uploaded_files,
        'pending_count': pending,
        'resolved_count': resolved,
    })


@login_required
def pending_questions(request):
    tickets = Ticket.objects.filter(status='pending').order_by('-created_at')
    return render(request, 'staff/pending.html', {
        'tickets': tickets,
        'pending_count': tickets.count(),
    })


@login_required
def resolved_questions(request):
    tickets = Ticket.objects.filter(status='resolved').order_by('-resolved_at')
    return render(request, 'staff/resolved.html', {
        'tickets': tickets,
        'resolved_count': tickets.count(),
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

    return redirect('staff_pending')


@login_required
def upload_pdf(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        file_bytes = file.read()
        file.seek(0)

        uploaded_file = UploadedFile.objects.create(
            filename=file.name,
            uploaded_file=ContentFile(file_bytes, name=file.name),
            uploaded_by=request.user.username,
        )

        result = process_pdf_and_upload(file_bytes, file.name)
        uploaded_file.status = 'success' if result.get('status') == 'success' else 'failed'
        uploaded_file.chunks = result.get('chunks', 0)
        uploaded_file.message = result.get('message', '')
        uploaded_file.save()

        return JsonResponse(result)

    return JsonResponse({"error": "No file provided"}, status=400)


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
    return JsonResponse({"error": "Method not allowed"}, status=405)
