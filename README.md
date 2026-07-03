# python-untis-extended

Functions:
- timetable
- homeworks
- school search
- Custom exceptions and objects

## Installation
pip install python-untis-extended

## Usage
untis = Untis()
homeworks = untis.homework.get_homework(start_date=date(2026, 4, 1), end_date=date(2026, 6, 29))
timetable = untis.timetable.get_timetable(start_date=date(2026, 6, 29), end_date=date(2026, 7, 1))

### Disclaimer
This is an unofficial, independent project and is not affiliated with, endorsed by, or approved by Untis. “Untis” is a trademark of its respective owner, used here only for identification purposes. This library may be changed or discontinued at any time, especially in case of trademark or legal concerns. No warranties provided. Users are responsible for compliance with applicable terms and laws.
