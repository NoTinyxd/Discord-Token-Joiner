import requests


class Solver:
    def __init__(self, api_url):
        self.api_url = api_url
        self.passed = False
        self.token = None
        self.res_json = None

    def solve(self, sitekey, hostname, rqdata):

        response = requests.post(
            self.api_url,
            json={
                "sitekey": sitekey,
                "hostname": hostname,
                "rqdata": rqdata,
            },
            timeout=6000,
        )

        response.raise_for_status()

        self.res_json = response.json()
        self.passed = self.res_json.get("success", False)
        self.token = self.res_json.get("token")

        return self.res_json
