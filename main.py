import session
import objects
import homework
import timetable
import schoolsearch


class Untis():
    def __init__(self) -> None:
        self.sesion = session.session()
        self.homework = homework.Homework(self.sesion)
        self.timetable = timetable.Timetable(self.sesion)
        self.schoolsearch = schoolsearch.SchoolSearch() # No session needed