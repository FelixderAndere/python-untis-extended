
# example usage: untis.homework.get_homework("2023-01-01", "2023-01-31")
class Homework():
    def __init__(self, session):
        self.session = session

    def get_homework(self, start_date: str, end_date: str):
        try:
            response = self.session.send_request(endpoint="/api/homeworks/lessons", params={"startDate": start_date, "endDate": end_date})
            return response.text[:500]
        except Exception as e:
            print(f"Error occurred while fetching homework: {e}")
            return None