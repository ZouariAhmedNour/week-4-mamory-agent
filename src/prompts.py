from src.models import StudentMemory

SYSTEM_PROMPT = """
Tu es un assistant étudiant personnel, bienveillant et concret.

Règles obligatoires :
- Utilise TOUJOURS la mémoire ci-dessous si elle contient des informations.
- Adapte tes conseils à la matière, au niveau et aux difficultés connues.
- Si la mémoire est vide, pose des questions pour apprendre à connaître l'étudiant.
- Réponds en français, reste concis et actionnable.
"""


def build_system_prompt(memory: StudentMemory) -> str:
    if memory.is_empty():
        memoire_txt = "Aucune information connue sur l'étudiant pour l'instant."
    else:
        lignes = []
        if memory.name:
            lignes.append(f"Nom : {memory.name}")
        if memory.matiere:
            lignes.append(f"Matière préparée : {memory.matiere}")
        if memory.niveau:
            lignes.append(f"Niveau : {memory.niveau}")
        if memory.difficultes:
            lignes.append(f"Difficultés connues : {', '.join(memory.difficultes)}")
        if memory.planning:
            lignes.append(f"Planning : {', '.join(memory.planning)}")
        memoire_txt = "\n".join(lignes)

    return f"{SYSTEM_PROMPT}\nMémoire actuelle sur l'étudiant :\n{memoire_txt}\n"


EXTRACTION_PROMPT = """
Tu es un extracteur d'informations. On te donne un échange entre un étudiant
et un assistant. Identifie les NOUVELLES informations sur l'étudiant apparues
dans ce dernier échange (pas celles déjà connues).

Réponds UNIQUEMENT avec un objet JSON de cette forme exacte :
{{
  "name": string ou null,
  "matiere": string ou null,
  "niveau": string ou null,
  "nouvelles_difficultes": [liste de strings, vide si aucune],
  "nouveau_planning": [liste de strings, vide si aucune]
}}

Message de l'étudiant : {user_message}
Réponse de l'assistant : {assistant_message}
"""


def build_extraction_prompt(user_message: str, assistant_message: str) -> str:
    return EXTRACTION_PROMPT.format(
        user_message=user_message,
        assistant_message=assistant_message,
    )