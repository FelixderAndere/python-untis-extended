from datetime import date
import json
import objects as objects
import errors as errors

class Timetable():
    def __init__(self, session):
        self.session = session

    def get_timetable(self, start_date: date, end_date: date):
        """
        Fetches the timetable for the specified date range.
        
        :param start_date: The start date for the timetable.
        :param end_date: The end date for the timetable.
        :return: An instance of objects.TimetableWeek.
        :raises UntisError: Any child exception from errors.py depending on the failure mode.
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

        try:
            payload = response.json()
        except (json.JSONDecodeError, ValueError) as e:
            raise errors.UntisDataError("Received a non-JSON response from the timetable API.") from e

        try:
            return objects.TimetableWeek.from_dict(payload)
        except Exception as e:
            raise errors.UntisDataError(
                f"Failed to map JSON data into a TimetableWeek object structure. Inner error: {e}"
            ) from e

    def _get_resource_type(self, jwt_claims: dict) -> str:
        types = str(jwt_claims.get("roles", "")).upper()
        for r_type in ("STUDENT", "TEACHER"):
            if r_type in types:
                return r_type
        return "STUDENT"