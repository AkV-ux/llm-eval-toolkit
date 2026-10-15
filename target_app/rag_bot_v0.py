import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL = "openai/gpt-oss-20b"

# 1. Read the document from disk
with open("target_app/policy.txt", encoding="utf-8") as f:
    document = f.read()

# 2. The rules for the bot, with the document included
SYSTEM_PROMPT = f"""You are a customer support assistant for Sunrise Electronics.
Answer ONLY using the document below.
If the answer is not in the document, reply exactly: I don't have that information.

DOCUMENT:
{document}
"""

def ask(question):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question},
        ],
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    questions = [
        "How many days do I have to return a product?",
        "Do you sell gaming consoles?",
    ]
    for q in questions:
        print("Q:", q)
        print("A:", ask(q))
        print("-" * 60)