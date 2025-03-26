from requests import get


class RofApiChecker:
    def __init__(self):
        pass

    def get_response(self):
        return get(
            "https://isitreadonlyfriday.com/api/isitreadonlyfriday/EST", timeout=5
        )
