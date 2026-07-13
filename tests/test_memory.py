from src.memory import read_memory, reset_memory, save_memory, update_memory
from src.models import StudentMemory


def test_read_memory_returns_empty_when_file_missing(tmp_path):
    fake_path = tmp_path / "memory.json"
    result = read_memory(path=fake_path)
    assert result.is_empty()


def test_save_then_read_memory(tmp_path):
    fake_path = tmp_path / "memory.json"
    save_memory(StudentMemory(name="Ahmed", matiere="Science"), path=fake_path)

    reloaded = read_memory(path=fake_path)
    assert reloaded.name == "Ahmed"
    assert reloaded.matiere == "Science"


def test_update_memory_appends_to_lists_without_duplicates(tmp_path):
    fake_path = tmp_path / "memory.json"
    save_memory(StudentMemory(difficultes=["Questions ouvertes"]), path=fake_path)

    updated = update_memory(
        path=fake_path,
        nouvelles_difficultes=["Questions ouvertes", "Gestion du temps"],
    )
    assert updated.difficultes == ["Questions ouvertes", "Gestion du temps"]


def test_reset_memory_clears_everything(tmp_path):
    fake_path = tmp_path / "memory.json"
    save_memory(StudentMemory(name="Ahmed"), path=fake_path)

    reset = reset_memory(path=fake_path)
    assert reset.is_empty()