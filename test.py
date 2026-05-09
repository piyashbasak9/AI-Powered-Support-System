import google.generativeai as genai

genai.configure(api_key="AIzaSyBrcEWaOjR24zJOqYe1w4Ja5x1xrnNDNzc")   # আপনার পুরনো কী (রিভোক করার আগে টেস্ট করুন)
model = genai.GenerativeModel('gemini-1.5-pro')
response = model.generate_content("Hello")
print(response.text)