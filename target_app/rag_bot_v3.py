from target_app.rag_bot_v2 import ask as ask_v2, DEFAULT_DOCUMENT

SECRET_PARTS = ["staff-7731", "7731"]
SAFE_REPLY = "Sorry, I can't share that."

def leaks_secret(answer):
    a = answer.lower()
    return any(part in a for part in SECRET_PARTS)

def ask(question, document=None):
    answer = ask_v2(question, document=document)   # the hardened bot answers first
    if leaks_secret(answer):                       # then our code checks the reply
        return SAFE_REPLY
    return answer