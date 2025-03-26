import os
import requests


class CapybaraDB:
    """Client for interacting with CapybaraDB.

    Requires CAPYBARA_PROJECT_ID and CAPYBARA_API_KEY environment variables.
    """

    def __init__(self):
        """Initialize CapybaraDB client from environment variables."""
        self.project_id = os.getenv("CAPYBARA_PROJECT_ID", "")
        self.api_key = os.getenv("CAPYBARA_API_KEY", "")

        if not self.project_id:
            raise ValueError(
                "Missing Project ID: Please provide the Project ID as an argument or set it in the CAPYBARA_PROJECT_ID environment variable. "
                "Tip: Ensure your environment file (e.g., .env) is loaded."
            )

        # Import appropriate classes based on whether API key is present
        if self.api_key:
            from ._hosted._database import Database
        else:
            from ._local._database import Database

        # Make these classes available at the instance level
        self.Database = Database

    def db(self, db_name: str):
        """Get database by name."""
        return self.Database(self.api_key, self.project_id, db_name)

    def __getattr__(self, name):
        """Allow db access via attribute: client.my_database"""
        return self.db(name)

    def __getitem__(self, name):
        """Allow db access via dictionary: client["my_database"]"""
        return self.db(name)
