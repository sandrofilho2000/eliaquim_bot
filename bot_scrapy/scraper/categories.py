import requests
from dotenv import load_dotenv
import os

class Categories:
    load_dotenv()
    API_URL = os.getenv("API_URL")
    API_KEY = os.getenv("API_KEY")
    
    def _load_categories(self):
        response = requests.get(
            f"{self.API_URL}/api/categories/",
            headers={"Authorization": f"Api-Key {self.API_KEY}"},
            timeout=10,
        )
        response.raise_for_status()
        return response.json()
    