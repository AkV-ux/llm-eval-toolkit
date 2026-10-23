import os
from dotenv import load_dotenv
from groq import Groq
from target_app.rag_bot_v3 import ask as ask_v3, DEFAULT_DOCUMENT

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

GUARD_MODEL = "meta-llama/llama-prompt-guard-2-86m"
THRESHOLD = 0.5
BLOCK_REPLY = "Sorry, I can't help with that request."

def injection_score(text):
    response = client.chat.completions.create(
        model=GUARD_MODEL,
        messages=[{"role": "user", "content": text}],
    )
    return float(response.choices[0].message.content)

def ask(question, document=None):
    if injection_score(question) >= THRESHOLD:   # check the input first
        return BLOCK_REPLY
    return ask_v3(question, document=document)   # then the hardened bot + output filter