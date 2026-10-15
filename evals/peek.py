from target_app.rag_bot_v0 import ask

questions = [
    "My laptop got wet and stopped working. Is it covered by warranty?",
    "How much extra will express shipping cost on a 7000 rupee order?",
    "I never opened my product. Can I still return it after 20 days?",
]

for q in questions:
    print("Q:", q)
    print("A:", ask(q))
    print("-" * 60)