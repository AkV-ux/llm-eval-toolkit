from target_app.rag_bot_v0 import ask

question = "I never opened my product. Can I still return it after 20 days?"

for i in range(5):
    print(f"Run {i + 1}:", ask(question))
    print()