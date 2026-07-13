from datetime import datetime
from typing import List, Literal, Optional

from pydantic import BaseModel, Field


class StudentMemory(BaseModel):
    """Mémoire long-terme (LTM) de l'étudiant."""

    name: Optional[str] = None
    matiere: Optional[str] = None
    niveau: Optional[str] = None
    difficultes: List[str] = Field(default_factory=list)
    planning: List[str] = Field(default_factory=list)

    def is_empty(self) -> bool:
        return (
            self.name is None
            and self.matiere is None
            and self.niveau is None
            and not self.difficultes
            and not self.planning
        )


class ConversationTurn(BaseModel):
    """Un tour de dialogue (mémoire court-terme, en RAM uniquement)."""

    role: Literal["user", "assistant"]
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)


class MemoryUpdate(BaseModel):
    """Ce que Gemini doit renvoyer pour dire ce qui a changé."""

    name: Optional[str] = None
    matiere: Optional[str] = None
    niveau: Optional[str] = None
    nouvelles_difficultes: List[str] = Field(default_factory=list)
    nouveau_planning: List[str] = Field(default_factory=list)