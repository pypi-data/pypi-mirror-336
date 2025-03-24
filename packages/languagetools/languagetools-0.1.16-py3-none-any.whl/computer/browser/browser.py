import requests
from .advanced import advanced_browser

class Browser:
    def __init__(self, computer):
        self.computer = computer
        self.installed_dependencies = False

    def search(self, query):
        """
        Searches the web for the specified query and returns the results.
        """
        headers = {"Authorization": f"Bearer {self.computer.api_key}"}
        response = requests.post(
            f'{self.computer.api_base}/tools/',
            json={"tool": "search", "input": {"query": query}},
            headers=headers
        )
        response_json = response.json()
        if "output" not in response_json:
            raise Exception(f"Error: {response_json}")
        return response_json["output"]

    def ai(self, task):
        """
        Operates a browser to accomplish the task.
        """
        return advanced_browser(self, task, self.computer.api_key, self.computer.api_base+"/openai")