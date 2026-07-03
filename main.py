import session
import objects
import homework
import timetable
import schoolsearch
from dotenv import load_dotenv
import os

load_dotenv()

class Untis():
    def __init__(self, base_url, username, password) -> None:
        self.sesion = session.session(base_url=base_url, username=username, password=password)


if __name__ == "__main:__":
    U = Untis(base_url=os.getenv("UNTIS_USERNAME"), username=os.getenv("UNTIS_USERNAME"), password=os.getenv("UNTIS_PASSWORD"))
