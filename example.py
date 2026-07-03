from main import Untis
from dotenv import load_dotenv
import os
from datetime import date

load_dotenv()

def test_homework():
    untis = Untis(base_url=os.getenv("BASE_URL"), username=os.getenv("UNTIS_USERNAME"), password=os.getenv("UNTIS_PASSWORD"))
    homeworks = untis.homework.get_homework(start_date=date(2026, 4, 1), end_date=date(2026, 6, 29))
    print("homeworks", homeworks)
    untis.session.logout()


def test_timetable():
    untis = Untis(base_url=os.getenv("BASE_URL"), username=os.getenv("UNTIS_USERNAME"), password=os.getenv("UNTIS_PASSWORD")) 
    timetable = untis.timetable.get_timetable(start_date=date(2026, 6, 29), end_date=date(2026, 7, 1))
    if timetable is None:
        print("timetable request failed")
        untis.session.logout()
        return

    print("days in week", len(timetable.days))
    print("lessons in week", len(timetable.lessons.lessons))

    if timetable.days and timetable.days[0].lessons.lessons:
        first_lesson = timetable.days[0].lessons.lessons[0]
        print("first lesson subjects", first_lesson.subjects)
        print("first lesson teachers", first_lesson.teachers)
        print("first lesson time", first_lesson.start, "->", first_lesson.end)

    print("timetable", timetable)
    untis.session.logout()



if __name__ == "__main__":
    test_timetable()