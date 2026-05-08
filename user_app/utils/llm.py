import google.generativeai as genai
from django.conf import settings
from shared.constants import LLM_MODEL, LLM_TEMPERATURE

genai.configure(api_key=settings.GEMINI_API_KEY)

def generate_answer(query, context):
    prompt = f"""Answer based ONLY on context. If answer not in context, respond: NO_INFO

Context: {context}
Question: {query}
Answer:"""
    
    model = genai.GenerativeModel(LLM_MODEL)
    response = model.generate_content(prompt, generation_config=genai.types.GenerationConfig(temperature=LLM_TEMPERATURE))
    return response.text.strip()