import os
import requests
from dotenv import load_dotenv

load_dotenv()

class GitLabAPIClient:
    def __init__(self):
        self.base_url = os.getenv("GITLAB_URL")
        self.token = os.getenv("PRIVATE_TOKEN")
        self.headers = {"PRIVATE-TOKEN": self.token}

    def _paginated_get(self, endpoint, params=None):
        results = []
        page = 1
        while True:
            response = requests.get(
                f"{self.base_url}/api/v4/{endpoint}",
                headers=self.headers,
                params={"page": page, "per_page": 100, **(params or {})}
            )
            response.raise_for_status()
            data = response.json()
            if not data:
                break
            results.extend(data)
            page += 1
        return results

    def get_external_users(self):
        """Fetch users with external identities (e.g., OAuth)"""
        return self._paginated_get("users", {"extern_uid": "*"})

    def get_project_tokens(self, project_id):
        """List access tokens for a project"""
        return self._paginated_get(f"projects/{project_id}/access_tokens")

    def get_group_audit_logs(self, group_id):
        """Retrieve audit events for a group"""
        return self._paginated_get(f"groups/{group_id}/audit_events")

# Example usage
if __name__ == "__main__":
    client = GitLabAPIClient()
    print("External users:", client.get_external_users())
    print("Project tokens:", client.get_project_tokens(123))
    print("Audit logs:", client.get_group_audit_logs(456))