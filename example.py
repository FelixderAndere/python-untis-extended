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
    timetable = untis.timetable.get_timetable(start_date=date(2026, 4, 1), end_date=date(2026, 4, 8))
    print("timetable", timetable)
    untis.session.logout()



if __name__ == "__main__":
    test_timetable()