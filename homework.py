from datetime import date
import objects

# example usage: untis.homework.get_homework("2023-01-01", "2023-01-31")
class Homework():
    def __init__(self, session):
        self.session = session

    def get_homework(self, start_date: date, end_date: date):
        homework_list = objects.HomeworkList([])
        try:
            response = self.session.send_request(endpoint="/api/homeworks/lessons", params={"startDate": start_date.strftime("%Y%m%d"), "endDate": end_date.strftime("%Y%m%d")})
            homeworks = response.get("data", {}).get("homeworks", [])
            for work in homeworks:
                homework_list.homeworks.append(objects.Homework.from_dict(work))
            return homework_list
        except Exception as e:
            print(f"Error occurred while fetching homework: {e}")
            return None