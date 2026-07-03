# Python-untis-extended

<p align="center">
  <a href="https://pypi.org">
    <img src="https://shields.io" alt="PyPI Version">
  </a>
  <a href="https://python.org">
    <img src="https://shields.io" alt="Python Version">
  </a>
  <a href="https://opensource.org">
    <img src="https://shields.io" alt="License">
  </a>
</p>

<p align="center">
  <b>A simple and object-oriented Python client for Untis.</b><br>
</p>

---

## Architecture & Capabilities

| Endpoint | Core Functionality
| :--- | :--- | :--- |
| `untis.timetable` | Period-accurate schedule extraction (with week and day objects)
| `untis.homework` | Fetching homeworks with detailed information
| `untis.schoolsearch` | Programmatic school search and server endpoint resolving

---

## Installation (WIP)

Deploy the stable distribution via the package manager:

```bash
pip install python-untis-extended
```

---

## Quick Start

```python
from datetime import date
from python_untis_extended import Untis

# Initialize the client instance
untis = Untis()

# Fetch active homework assignments within a date range
homeworks = untis.homework.get_homework(
    start_date=date(2026, 4, 1),
    end_date=date(2026, 6, 29)
)

# Retrieve the structured lesson schedule
timetable = untis.timetable.get_timetable(
    start_date=date(2026, 6, 29),
    end_date=date(2026, 7, 1)
)

print(homeworks)
print(timetable)
```

---

## Module Overview

### Timetable
Extracts structured lesson schedules for defined time ranges. The engine processes core metadata fields into clean object attributes, mapping subjects, physical rooms, assigned educators, and exact time intervals.

### Homework
Queries upcoming school assignments between two dates. Designed to feed automated notification systems, tracking dashboards, and planning applications.

### School Search
Provides the untis school search to easily fetch a school without need to know the exact untis school name

---

## ⚠️ Disclaimer

This is an **unofficial, independent project** and is not affiliated with, endorsed by, or approved by Untis. “Untis” is a trademark of its respective owner and is used here strictly for identification purposes. 
This library may be changed or discontinued at any time, especially due to legal or trademark concerns. No warranties are provided. Users are responsible for compliance with applicable terms and laws. 
It is a pure hobby / free-time project built mainly for fun and for use in a school context.
