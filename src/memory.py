from pathlib import Path

from src.config import get_env
from src.models import StudentMemory
from src.utils import load_json, save_json


def get_memory_path() -> Path:
    return Path(get_env("MEMORY_PATH", "data/memory.json"))


def read_memory(path: Path | None = None) -> StudentMemory:
    path = path or get_memory_path()
    raw = load_json(path)
    return StudentMemory(**raw)


def save_memory(memory: StudentMemory, path: Path | None = None) -> None:
    path = path or get_memory_path()
    save_json(path, memory.model_dump())


def update_memory(
    path: Path | None = None,
    name: str | None = None,
    matiere: str | None = None,
    niveau: str | None = None,
    nouvelles_difficultes: list[str] | None = None,
    nouveau_planning: list[str] | None = None,
) -> StudentMemory:
    path = path or get_memory_path()
    memory = read_memory(path)

    if name:
        memory.name = name
    if matiere:
        memory.matiere = matiere
    if niveau:
        memory.niveau = niveau

    if nouvelles_difficultes:
        for item in nouvelles_difficultes:
            if item not in memory.difficultes:
                memory.difficultes.append(item)

    if nouveau_planning:
        for item in nouveau_planning:
            if item not in memory.planning:
                memory.planning.append(item)

    save_memory(memory, path)
    return memory


def reset_memory(path: Path | None = None) -> StudentMemory:
    path = path or get_memory_path()
    empty = StudentMemory()
    save_memory(empty, path)
    return empty