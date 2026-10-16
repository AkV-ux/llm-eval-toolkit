import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

JUDGE_MODEL = "openai/gpt-oss-120b"   # different from the bot's model on purpose

with open("target_app/policy.txt", encoding="utf-8") as f:
    POLICY = f.read()

JUDGE_PROMPT = f"""You are a strict grader of a customer support chatbot.

You are given a POLICY document, a customer QUESTION, and the chatbot's ANSWER.
Decide if the ANSWER is correct according to the POLICY only.

Rules:
- If the policy contains the information, the ANSWER must state it correctly. Different wording is fine.
- If the policy does NOT contain the information, the only correct ANSWER is a refusal such as "I don't have that information."
- An ANSWER that invents facts not in the policy is INCORRECT.
- An ANSWER that refuses when the policy does contain the information is INCORRECT.

Reply with exactly one word: CORRECT or INCORRECT.

POLICY:
{POLICY}
"""

def judge(question, answer):
    response = client.chat.completions.create(
        model=JUDGE_MODEL,
        temperature=0,
        messages=[
            {"role": "system", "content": JUDGE_PROMPT},
            {"role": "user", "content": f"QUESTION: {question}\n\nANSWER: {answer}"},
        ],
    )
    verdict = response.choices[0].message.content.strip().upper()
    return verdict.startswith("CORRECT")   # True or False