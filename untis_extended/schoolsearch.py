import time
import requests
import json
import objects as objects

class SchoolSearch:
    def __init__(self):
        pass

    def search_school(self, search_query: str) -> objects.SchoolSearchResult:
        """
        Search for schools based on the provided search query with the untis school search
            :param search_query: The search query for the school search.
            :return: A dictionary containing the search results.
        """

        search_url = "https://schoolsearch.webuntis.com/schoolquery2"

        payload = {
            "id": f"wu_schulsuche-{int(time.time() * 1000)}",
            "jsonrpc": "2.0",
            "method": "searchSchool",
            "params": [{"search": search_query}]
        }

        headers = {"Content-Type": "application/json"}

        try:
            response = requests.post(search_url, json=payload, headers=headers, timeout=10)
            response.raise_for_status()

        except requests.RequestException as exc:
            raise (f"School search request failed: {exc}") from exc

        try:
            data = response.json()

        except json.JSONDecodeError as exc:
            raise (f"Invalid JSON response from school search") from exc

        schools = []

        for school in data.get("result", {}).get("schools", []):
            schools.append(objects.School.from_dict(school))


        return objects.SchoolSearchResult(
            query=search_query,
            count=len(schools),
            schools=schools
        )
