import json
from target_app.rag_bot_v1 import ask

REFUSAL = "i don't have that information"

def clean(text):
    # make curly apostrophes plain, and ignore capital letters
    return text.replace("’", "'").lower()

with open("datasets/qa_set.json", encoding="utf-8") as f:
    cases = json.load(f)

passed = 0
for case in cases:
    answer = ask(case["question"])
    a = clean(answer)

    if case["type"] == "answerable":
        ok = all(word.lower() in a for word in case["must_contain"])
    else:
        ok = REFUSAL in a

    passed += ok
    print("PASS" if ok else "FAIL", "|", case["question"])
    if not ok:
        print("      bot said:", answer)

print()
print(f"Score: {passed}/{len(cases)}")