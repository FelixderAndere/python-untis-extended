# python-untis-extended

![PyPI](https://img.shields.io/pypi/v/python-untis-extended?style=flat-square)
![Python](https://img.shields.io/badge/python-3.8%2B-blue?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)

A modern Python wrapper for accessing **Untis data** with extended features like timetables, homework handling, school search, and structured data models.

---

## Features

- Timetable retrieval
- Homework fetching
- School search
- Structured objects for clean data handling
- Custom exceptions for robust error handling
- Simple and developer-friendly API

---

## Installation

pip install python-untis-extended

---

## Quick Start

from datetime import date
from python_untis_extended import Untis

untis = Untis()

homeworks = untis.homework.get_homework(
    start_date=date(2026, 4, 1),
    end_date=date(2026, 6, 29)
)

timetable = untis.timetable.get_timetable(
    start_date=date(2026, 6, 29),
    end_date=date(2026, 7, 1)
)

print(homeworks)
print(timetable)

---

## Content

### Timetable

Retrieve structured lesson schedules for a given time range.  
Includes subjects, rooms, teachers, and time slots.

---

### Homework

Fetch homework assignments between two dates.  
Useful for tracking school tasks and planning ahead.

---

### School Search

Search for schools programmatically to simplify onboarding and configuration.

---

## Example Use Cases

- Student planning dashboards
- Homework tracking bots
- School organization tools
- Automation scripts for syncing timetables
- Educational productivity apps


---

## ⚠️ Disclaimer

This is an **unofficial, independent project** and is not affiliated with, endorsed by, or approved by Untis. “Untis” is a trademark of its respective owner and is used here strictly for identification purposes. 
This library may be changed or discontinued at any time, especially due to legal or trademark concerns. No warranties are provided. Users are responsible for compliance with applicable terms and laws. 
It is a pure hobby / free-time project built mainly for fun and for use in a school context.