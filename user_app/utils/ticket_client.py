import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

def create_ticket(ticket_id, query, extracted_text="", file_info=None):
    try:
        response = requests.post(
            settings.STAFF_SERVER_URL,
            data={
                "ticket_id": ticket_id,
                "query": query,
                "extracted_text": extracted_text,
                "file_info": file_info
            },
            timeout=10
        )
        return response.status_code == 201
    except Exception as e:
        logger.error(f"Ticket creation failed: {e}")
        return False