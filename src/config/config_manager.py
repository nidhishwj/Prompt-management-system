import os
from dotenv import load_dotenv

#Load environment variables from the .env file

load_dotenv()

class ConfigManager:
    def __init__(self):
        self.load()

    def load(self):
        """Loads the .env file."""
        load_dotenv()

    def get(self, key: str, default: str = None) -> dict[str,str]:
        """Fetches the environment variable."""
        return os.getenv (key, default)