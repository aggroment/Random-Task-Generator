from enum import Enum
from dataclasses import dataclass
from datetime import datetime
import json

class TaskType(Enum):
    WORK = "Работа"
    SPORT = "Спорт"
    STUDY = "Учеба"
    OTHER = "Другое"

class Difficulty(Enum):
    EASY = "Лёгкая"
    MEDIUM = "Средняя"
    HARD = "Сложная"

@dataclass
class Task:
    description: str
    type: TaskType
    difficulty: Difficulty
    created_at: str = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            "description": self.description,
            "type": self.type.value,
            "difficulty": self.difficulty.value,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            description=data["description"],
            type=TaskType(data["type"]),
            difficulty=Difficulty(data["difficulty"]),
            created_at=data["created_at"]
        )

    def __str__(self):
        return f"[{self.type.value}] {self.description} (Сложность: {self.difficulty.value}) - {self.created_at}"
