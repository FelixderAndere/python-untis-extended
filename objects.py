from dataclasses import dataclass
from datetime import datetime, date
from typing import Any

@dataclass
class Homework:
    id: int
    text: str
    date: "date"
    due_date: "date"
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


def _extract_position_short_names(entry: dict[str, Any], position_key: str) -> list[str]:
    values = []
    for item in entry.get(position_key) or []:
        current = item.get("current") or {}
        short_name = current.get("shortName")
        if short_name:
            values.append(short_name)
    return values


@dataclass
class Lesson:
    ids: list[int]
    start: datetime
    end: datetime
    lesson_type: str
    status: str
    teachers: list[str]
    subjects: list[str]
    rooms: list[str]
    classes: list[str]
    notes: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Lesson":
        duration = data.get("duration", {})
        start = datetime.fromisoformat(duration["start"])
        end = datetime.fromisoformat(duration["end"])

        return cls(
            ids=data.get("ids", []),
            start=start,
            end=end,
            lesson_type=data.get("type", ""),
            status=data.get("status", ""),
            teachers=_extract_position_short_names(data, "position1"),
            subjects=_extract_position_short_names(data, "position2"),
            rooms=_extract_position_short_names(data, "position3"),
            classes=_extract_position_short_names(data, "position4"),
            notes=data.get("notesAll", ""),
        )


@dataclass
class LessonList:
    lessons: list[Lesson]


@dataclass
class TimetableDay:
    day: date
    resource_type: str
    resource_id: int | None
    status: str
    lessons: LessonList

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TimetableDay":
        entries = data.get("gridEntries", [])
        lessons = [Lesson.from_dict(entry) for entry in entries]
        resource = data.get("resource", {})

        return cls(
            day=datetime.fromisoformat(data["date"]).date(),
            resource_type=data.get("resourceType", ""),
            resource_id=resource.get("id"),
            status=data.get("status", ""),
            lessons=LessonList(lessons=lessons),
        )


@dataclass
class TimetableWeek:
    days: list[TimetableDay]
    lessons: LessonList

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TimetableWeek":
        day_objects = [TimetableDay.from_dict(day) for day in data.get("days", [])]

        lesson_objects = []
        for day in day_objects:
            lesson_objects.extend(day.lessons.lessons)

        return cls(days=day_objects, lessons=LessonList(lessons=lesson_objects))

