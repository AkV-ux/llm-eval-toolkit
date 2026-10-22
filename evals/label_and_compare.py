import json
from target_app.rag_bot_v1 import ask
from evals.judge import judge

with open("datasets/qa_set.json", encoding="utf-8") as f:
    questions = [c["question"] for c in json.load(f)]

# extra tricky questions
questions += [
    "What is the warranty on headphones?",
    "I opened my phone and used it for a week. Can I return it after 10 days?",
    "Do you ship on Sundays?",
    "Is express shipping free on orders above 5000 rupees?",
]

print("Keep target_app/policy.txt open to check each answer.")
print("Type y = correct, n = wrong, s = skip if you are unsure.\n")

records = []
for q in questions:
    a = ask(q)
    print("QUESTION:", q)
    print("ANSWER  :", a)
    while True:
        h = input("Correct per the policy? (y/n/s): ").strip().lower()
        if h in ("y", "n", "s"):
            break
    print()
    if h != "s":
        records.append((q, a, h == "y"))

print("Now checking the judge against your verdicts...\n")
agree = 0
for q, a, human in records:
    verdict = judge(q, a)
    if verdict == human:
        agree += 1
    else:
        print("MISMATCH |", q)
        print("   bot said:", a)
        print("   you:", human, "| judge:", verdict)

print()
print(f"Judge agrees with you on {agree}/{len(records)} answers")