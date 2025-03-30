import os
import argparse
import requests
import time
from dotenv import load_dotenv

load_dotenv()

class GitLabAPIClient:
    def __init__(self):
        self.base_url = os.getenv("GITLAB_URL")
        self.token = os.getenv("PRIVATE_TOKEN")
        self.headers = {"PRIVATE-TOKEN": self.token}
        self.rate_limit_delay = 2 

    def _paginated_get(self, endpoint, params=None):
        """Handles pagination for GitLab API endpoints.
        Docs: https://docs.gitlab.com/ee/api/#pagination"""
        results = []
        page = 1
        while True:
            try:
                response = requests.get(
                    f"{self.base_url}/api/v4/{endpoint}",
                    headers=self.headers,
                    params={"page": page, "per_page": 100, **(params or {})}
                )
                
                if response.status_code == 429:
                    retry_after = int(response.headers.get("Retry-After", 30))
                    print(f"Rate limited. Retrying after {retry_after} seconds...")
                    time.sleep(retry_after)
                    continue
                
                response.raise_for_status()
                data = response.json()
                
                if not data:
                    break
                
                results.extend(data)
                page += 1
                time.sleep(self.rate_limit_delay)
                
            except requests.exceptions.RequestException as e:
                print(f"API request failed: {str(e)}")
                break
        
        return results


    def get_external_users(self):
        """Fetch users with external identities (SAML/OAuth). 
        Docs: https://docs.gitlab.com/ee/api/users.html#list-users"""
        users = self._paginated_get("users")
        return [user for user in users if user.get("external") is True]


    def get_project_tokens(self, project_id):
        """List access tokens for a project. 
        Docs: https://docs.gitlab.com/ee/api/project_access_tokens.html"""
        return self._paginated_get(f"projects/{project_id}/access_tokens")

    def get_pipelines(self, project_id):
        """List CI/CD pipelines for a project. 
        Docs: https://docs.gitlab.com/ee/api/pipelines.html"""
        return self._paginated_get(f"projects/{project_id}/pipelines")

    def get_webhooks(self, project_id):
        """List project webhooks. 
        Docs: https://docs.gitlab.com/ee/api/projects.html#list-project-hooks"""
        return self._paginated_get(f"projects/{project_id}/hooks")

    def get_instance_audit_logs(self):
        """Retrieve instance-wide audit events (GitLab Premium only). 
        Docs: https://docs.gitlab.com/ee/api/audit_events.html"""
        try:
            return self._paginated_get("audit_events")
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                print("Audit logs require GitLab Premium. Check /var/log/gitlab/gitlab-rails/audit_json.log")
            return []

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audit GitLab external access")
    parser.add_argument("--project-id", type=int, required=True, help="Project ID to audit")
    parser.add_argument("--group-id", type=int, help="Group ID to audit (optional)")
    args = parser.parse_args()

    client = GitLabAPIClient()
    
    print("\n=== External Users ===")
    print(client.get_external_users())
    
    print("\n=== Project Access Tokens ===")
    print(client.get_project_tokens(args.project_id))
    
    print("\n=== CI/CD Pipelines ===")
    print(client.get_pipelines(args.project_id))
    
    print("\n=== Webhooks ===")
    print(client.get_webhooks(args.project_id))
    
    print("\n=== Instance Audit Logs ===")
    print(client.get_instance_audit_logs())