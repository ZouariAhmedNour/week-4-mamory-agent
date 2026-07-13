import json

from google.genai import types

from src.config import get_env, get_gemini_client
from src.memory import read_memory, reset_memory, update_memory
from src.models import ConversationTurn, MemoryUpdate
from src.prompts import build_extraction_prompt, build_system_prompt
from src.utils import pretty_print


def build_contents(history: list[ConversationTurn], user_message: str) -> list[types.Content]:
    contents = []
    for turn in history:
        role = "user" if turn.role == "user" else "model"
        contents.append(types.Content(role=role, parts=[types.Part(text=turn.content)]))
    contents.append(types.Content(role="user", parts=[types.Part(text=user_message)]))
    return contents


def get_response(system_prompt: str, history: list[ConversationTurn], user_message: str) -> str:
    client = get_gemini_client()
    model = get_env("GEMINI_MODEL", "gemini-2.5-flash")
    contents = build_contents(history, user_message)

    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=types.GenerateContentConfig(system_instruction=system_prompt),
    )
    return response.text.strip()


def extract_memory_updates(user_message: str, assistant_message: str) -> MemoryUpdate:
    client = get_gemini_client()
    model = get_env("GEMINI_MODEL", "gemini-2.5-flash")
    prompt = build_extraction_prompt(user_message, assistant_message)

    try:
        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config=types.GenerateContentConfig(response_mime_type="application/json"),
        )
        data = json.loads(response.text)
        return MemoryUpdate(**data)
    except Exception as error:
        print(f"⚠️  Extraction mémoire ignorée : {error}")
        return MemoryUpdate()


def print_help() -> None:
    print(
        "\nCommandes disponibles :\n"
        "  show   -> afficher la mémoire actuelle\n"
        "  reset  -> réinitialiser la mémoire\n"
        "  help   -> afficher cette aide\n"
        "  quit   -> quitter\n"
    )


def run() -> None:
    current_memory = read_memory()
    history: list[ConversationTurn] = []

    print("🎓 Assistant étudiant (Week 4 - Memory). Tape 'help' pour les commandes.\n")

    while True:
        user_message = input("Toi > ").strip()

        if not user_message:
            continue
        if user_message.lower() == "quit":
            print("👋 À bientôt !")
            break
        if user_message.lower() == "help":
            print_help()
            continue
        if user_message.lower() == "show":
            pretty_print(current_memory.model_dump())
            continue
        if user_message.lower() == "reset":
            current_memory = reset_memory()
            history.clear()
            print("🧹 Mémoire réinitialisée.")
            continue

        system_prompt = build_system_prompt(current_memory)
        assistant_message = get_response(system_prompt, history, user_message)
        print(f"Agent > {assistant_message}\n")

        history.append(ConversationTurn(role="user", content=user_message))
        history.append(ConversationTurn(role="assistant", content=assistant_message))

        update = extract_memory_updates(user_message, assistant_message)
        current_memory = update_memory(
            name=update.name,
            matiere=update.matiere,
            niveau=update.niveau,
            nouvelles_difficultes=update.nouvelles_difficultes,
            nouveau_planning=update.nouveau_planning,
        )


if __name__ == "__main__":
    run()