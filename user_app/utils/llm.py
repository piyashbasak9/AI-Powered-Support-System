import os
import time
from openai import OpenAI
from django.conf import settings
from shared.constants import LLM_MODEL, LLM_TEMPERATURE

GROQ_API_KEY = settings.GROQ_API_KEY or os.getenv('GROQ_API_KEY', '')
if not GROQ_API_KEY:
    raise RuntimeError("Groq API key is missing. Set GROQ_API_KEY.")

client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

def generate_answer(query, context):
    prompt = f"""Answer detail based ONLY on context. If answer not in context, respond: NO_INFO

Context: {context}
Question: {query}
Answer:"""
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=LLM_MODEL,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=LLM_TEMPERATURE,
                max_tokens=1000
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                time.sleep(wait_time)
                continue
            raise RuntimeError(f"Groq generation failed after {max_retries} attempts: {e}") from e