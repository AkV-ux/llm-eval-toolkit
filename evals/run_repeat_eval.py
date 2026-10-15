from target_app.rag_bot_v0 import ask

RUNS = 5

def clean(text):
    return text.replace("’", "'").lower()

# each test = a question + a one-line rule for what a good answer looks like
tests = [
    ("My laptop got wet and stopped working. Is it covered by warranty?",
     lambda a: "not covered" in a or "isn't covered" in a),
    ("How much extra will express shipping cost on a 7000 rupee order?",
     lambda a: "299" in a),
    ("I never opened my product. Can I still return it after 20 days?",
     lambda a: "14" in a and any(w in a for w in ["cannot", "can't", "not be eligible", "not eligible", "expired", "closed", "no,", "no—"])),
]

for question, is_good in tests:
    good = 0
    failures = []
    for _ in range(RUNS):
        answer = clean(ask(question))
        if is_good(answer):
            good += 1
        else:
            failures.append(answer)
    print(f"{good}/{RUNS} good | {question}")
    for f in failures:
        print("     FAILED ANSWER:", f)