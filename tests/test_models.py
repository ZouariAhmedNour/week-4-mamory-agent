import pytest
from pydantic import ValidationError

from src.models import ConversationTurn, MemoryUpdate, StudentMemory


def test_student_memory_default_is_empty():
    memory = StudentMemory()
    assert memory.is_empty() is True


def test_student_memory_not_empty_when_filled():
    memory = StudentMemory(matiere="Science")
    assert memory.is_empty() is False


def test_conversation_turn_requires_valid_role():
    turn = ConversationTurn(role="user", content="Salut")
    assert turn.role == "user"

    with pytest.raises(ValidationError):
        ConversationTurn(role="robot", content="Invalide")


def test_memory_update_defaults_are_empty():
    update = MemoryUpdate()
    assert update.nouvelles_difficultes == []
    assert update.nouveau_planning == []