from django.db import models
import uuid

class QueryLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    query = models.TextField()
    response_status = models.CharField(max_length=50)
    ticket_id = models.CharField(max_length=36, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']