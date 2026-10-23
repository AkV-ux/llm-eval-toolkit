import json
import time
from target_app.rag_bot_v2 import ask
from evals.judge import judge

REFUSAL = "i don't have that information"

def clean(text):
    return text.replace("’", "'").lower()

with open("datasets/qa_set.json", encoding="utf-8") as f:
    cases = json.load(f)

keyword_pass = 0
judge_pass = 0

for case in cases:
    answer = ask(case["question"])
    a = clean(answer)

    if case["type"] == "answerable":
        keyword_ok = all(w.lower() in a for w in case["must_contain"])
    else:
        keyword_ok = REFUSAL in a

    judge_ok = judge(case["question"], answer)
    if not judge_ok:
        print("JUDGE SAYS WRONG |", case["question"])
        print("   bot said:", answer)

    keyword_pass += keyword_ok
    judge_pass += judge_ok

    if keyword_ok != judge_ok:
        print("DISAGREE |", case["question"])
        print("   bot said:", answer)
        print("   keyword:", keyword_ok, "| judge:", judge_ok)
    time.sleep(0.5)  # small pause to be kind to the free tier

print()
print(f"Keyword scorer: {keyword_pass}/{len(cases)}")
print(f"LLM judge:      {judge_pass}/{len(cases)}")