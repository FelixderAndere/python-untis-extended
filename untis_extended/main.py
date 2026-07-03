import session as session
import objects as objects
import homework as homework
import timetable as timetable
import schoolsearch as schoolsearch
from dotenv import load_dotenv
import os

load_dotenv()

class Untis():
    def __init__(self, base_url, username, password) -> None:
        self.session = session.session(base_url=base_url, username=username, password=password)
        print("self session", self.session.jsessionid)
        self.homework = homework.Homework(self.session)
        self.timetable = timetable.Timetable(self.session)
        self.schoolsearch = schoolsearch.SchoolSearch()