from dataclasses import dataclass
from datetime import datetime, date

from dataclasses import dataclass
from datetime import date

@dataclass
class Homework:
    id: int
    text: str
    date: datetime.date
    due_date: datetime.date
    lesson_id: int
    completed: bool = False

    @classmethod
    def from_dict(cls, data: dict) -> "Homework":
        return cls(
            id=data["id"],
            text=data["text"],
            date=datetime.strptime(str(data["date"]), "%Y%m%d").date(),
            due_date=datetime.strptime(str(data["dueDate"]), "%Y%m%d").date(),
            lesson_id=data["lessonId"],
            completed=data.get("completed", False)
        )

@dataclass
class HomeworkList:
    homeworks: list[Homework]

