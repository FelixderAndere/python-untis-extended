from main import Untis

untis = Untis() 
homeworks = untis.homework.get_homework(start_date="2025-01-01", end_date="2026-06-31")
print("homeworks", homeworks)


def test_timetable():
    untis = Untis() 
    timetable = untis.homework.get_homework(start_date="2025-01-01", end_date="2026-06-31")
    print("homeworks", timetable)