from datetime import date


class Timetable():
    def __init__(self, session):
        self.session = session

    def get_timetable(self, start_date: date, end_date: date):
        """
        Fetches the timetable for the specified date range
        
        :param start_date: The start date for the timetable (optional).
        :param end_date: The end date for the timetable (optional).
        :return: A list of timetable entries.
        """
        # Implementation to fetch timetable data from Untis API
        response = self.session.send_request(endpoint="/api/rest/view/v1/timetable/entries", params={"start": start_date, "end": end_date, "resourceType": "STUDENT", "timetableType": "MY_TIMETABLE", "ressources": "1949", "layout": "START_TIME"})
        return response
