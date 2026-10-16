from evals.judge import judge

# (question, bot answer, what a human says the verdict should be)
examples = [
    ("My laptop got wet and stopped working. Is it covered by warranty?",
     "No. Water damage is explicitly excluded from the warranty.", True),
    ("How much extra does express shipping cost?",
     "Express shipping is free for all orders.", False),
    ("How long is the warranty on a smartwatch?",
     "Smartwatches carry a 1-year warranty.", False),
    ("How long is the warranty on a smartwatch?",
     "I don't have that information.", True),
    ("I never opened my product. Can I still return it after 20 days?",
     "Yes, you can return it within 30 days.", False),
    ("My laptop got wet and stopped working. Is it covered by warranty?",
     "I don't have that information.", False),
]

agree = 0
for question, answer, human in examples:
    verdict = judge(question, answer)
    match = verdict == human
    agree += match
    print("MATCH" if match else "MISMATCH", "| judge:", verdict, "| human:", human, "|", answer)

print()
print(f"Judge agrees with human: {agree}/{len(examples)}")