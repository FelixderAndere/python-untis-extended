from datetime import date
import json
import objects as objects
import errors as errors

class Homework():
    def __init__(self, session):
        self.session = session

    def get_homework(self, start_date: date, end_date: date):
        """
        Fetches homework data for the specified date range.
        
        :param start_date: The start date.
        :param end_date: The end date.
        :return: An instance of objects.HomeworkList containing homework records.
        :raises UntisError: Handles underlying network, auth, or schema validation failures.
        """
        response = self.session.send_request(
            endpoint="/api/homeworks/lessons", 
            params={
                "startDate": start_date.strftime("%Y%m%d"), 
                "endDate": end_date.strftime("%Y%m%d")
            }
        )

        try:
            payload = response.json()
        except (json.JSONDecodeError, ValueError) as e:
            raise errors.UntisDataError("Received a non-JSON response from the homework API.") from e

        homework_list = objects.HomeworkList([])
        try:
            homeworks_data = payload.get("data", {}).get("homeworks", [])
            
            for work in homeworks_data:
                homework_list.homeworks.append(objects.Homework.from_dict(work))
                
            return homework_list
            
        except Exception as e:
            raise errors.UntisDataError(
                f"Failed to parse homework data structure. The API schema may have changed. Inner error: {e}"
            ) from e