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

        response = self.session.send_request(
            endpoint="/api/rest/view/v1/timetable/entries",
            params={
                "start": start_date.isoformat(),
                "end": end_date.isoformat(),
                "format": "20",
                "resourceType": self._get_resource_type(self.session.jwt_claims),
                "resources": self.session.jwt_claims.get("person_id"),
                "periodTypes": "",
                "timetableType": "MY_TIMETABLE",
                "layout": "START_TIME",
            }
        )
        return response
    
    def _get_resource_type(self, jwt_claims):
        types = str(jwt_claims.get("roles", "")).upper()
        for type in ("STUDENT", "TEACHER"):
            if type in types:
                return type
