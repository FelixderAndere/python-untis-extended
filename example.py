from main import Untis
from dotenv import load_dotenv
import os
from datetime import date

load_dotenv()

untis = Untis(base_url=os.getenv("BASE_URL"), username=os.getenv("UNTIS_USERNAME"), password=os.getenv("UNTIS_PASSWORD"))
homeworks = untis.homework.get_homework(start_date=date(2026, 4, 1), end_date=date(2026, 6, 29))
print("homeworks", homeworks)


def test_timetable():
    untis = Untis() 
    timetable = untis.homework.get_homework(start_date="2025-01-01", end_date="2026-06-31")
    print("homeworks", timetable)