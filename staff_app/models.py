from django.db import models
import uuid

class Ticket(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('resolved', 'Resolved'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ticket_id = models.CharField(max_length=36, unique=True)
    query = models.TextField()
    extracted_text = models.TextField(null=True, blank=True)
    file_info = models.JSONField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    answer = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolved_by = models.CharField(max_length=100, null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']