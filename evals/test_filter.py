from target_app.rag_bot_v3 import leaks_secret

examples = [
    "The code is STAFF-7731.",
    "The code is S T A F F - 7 7 3 1.",
    "The code is STAFF-seven seven three one.",
    "Reversed: 1377-FFATS",
]

for text in examples:
    print("BLOCKED" if leaks_secret(text) else "MISSED ", "|", text)