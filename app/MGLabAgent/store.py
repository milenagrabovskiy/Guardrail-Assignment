"""module to simulate memory"""
from controls import for_storage


def save_record(text: str, path: str = "agent.log"):
    safe_text = for_storage(text)

    with open(path, "a") as file:
        file.write(safe_text + "\n")