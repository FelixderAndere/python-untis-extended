import requests

class session():
    def __init__(self, base_url) -> None:
        self.base_url = base_url
        self.login()

    def login(self):
        pass

    def send_request(self, endpoint, params):
        base_url = "..."

        url = f"{base_url}{endpoint}"

        headers = {
            "User-Agent": self.config["useragent"] or "",
            "Content-Type": "application/json",
        }

        if "jsessionid" in self.config:
            headers["Cookie"] = f'JSESSIONID={self.config["jsessionid"]}'
        else:
            raise errors.NotLoggedInError("No JSESSIONID found. Please log in first.")

        print("debug", f"Making custom request to {url} with params: {params}")

        response = requests.get(url, params=params, headers=headers)

        try:
            response_data = response.json()
            print("debug", f"Received valid JSON response: {str(response_data)[:100]}")
        except json.JSONDecodeError:
            raise errors.RemoteError("Invalid JSON response", response.text)

        return response_data
