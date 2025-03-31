import os
import argparse
import requests
import time
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()


class GitLabAPIClient:
    def __init__(self):
        self.base_url = os.getenv("GITLAB_URL")
        self.token = os.getenv("PRIVATE_TOKEN")
        self.headers = {"PRIVATE-TOKEN": self.token}
        self.rate_limit_delay = 2

    def _paginated_get(self, endpoint, params=None):
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

    def get_external_users(self, search=None):
        params = {"externals": True}
        if search:
            params["search"] = search
        users = self._paginated_get("users", params=params)
        return [user for user in users if user.get("external") is True]

    def get_project_tokens(self, project_id):
        return self._paginated_get(f"projects/{project_id}/access_tokens")

    def get_pipelines(self, project_id, ref=None, status=None):
        params = {}
        if ref:
            params["ref"] = ref
        if status:
            params["status"] = status
        return self._paginated_get(f"projects/{project_id}/pipelines", params=params)

    def get_webhooks(self, project_id):
        return self._paginated_get(f"projects/{project_id}/hooks")

    def get_instance_audit_logs(self):
        try:
            return self._paginated_get("audit_events")
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                print("Audit logs require GitLab Premium. Check /var/log/gitlab/gitlab-rails/audit_json.log")
            return []

    def check_token_expiry(self, project_id, days_threshold=30, token_name=None, created_before=None, created_after=None):
        tokens = self.get_project_tokens(project_id)
        soon_to_expire = []

        for token in tokens:
            if not token.get("expires_at"):
                continue

            expires_at = datetime.strptime(token["expires_at"], "%Y-%m-%d")
            if expires_at >= datetime.now() + timedelta(days=days_threshold):
                continue

            match = True

            if token_name and token_name.lower() not in token.get("name", "").lower():
                match = False

            if created_before:
                created_at = datetime.strptime(token["created_at"].split("T")[0], "%Y-%m-%d")
                if created_at >= datetime.strptime(created_before, "%Y-%m-%d"):
                    match = False

            if created_after:
                created_at = datetime.strptime(token["created_at"].split("T")[0], "%Y-%m-%d")
                if created_at <= datetime.strptime(created_after, "%Y-%m-%d"):
                    match = False

            if match:
                soon_to_expire.append({
                    "id": token["id"],
                    "name": token["name"],
                    "expires_at": token["expires_at"],
                    "created_at": token["created_at"]
                })

        return soon_to_expire


def display_section(title, data):
    print(f"\n=== {title} ===")
    if data is None:
        print("  No response received.")
    elif isinstance(data, list) and data:
        for idx, item in enumerate(data, start=1):
            print(f"\n[{title[:-1]} {idx}]")
            for key, value in item.items():
                print(f"  {key}: {value}")
    elif isinstance(data, dict) and data:
        for key, value in data.items():
            print(f"  {key}: {value}")
    else:
        print("  No data found.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audit GitLab external access")
    parser.add_argument("--project-id", type=int, required=True, help="Project ID to audit")
    parser.add_argument("--group-id", type=int, help="Group ID to audit (optional)")
    parser.add_argument("--search-user", type=str, help="Search external users by name/email")
    parser.add_argument("--ref", type=str, help="Filter pipelines by ref")
    parser.add_argument("--status", type=str, help="Filter pipelines by status")
    parser.add_argument("--check-token-expiry", action="store_true", help="Check for soon-to-expire project tokens")
    parser.add_argument("--token-name", type=str, help="Filter tokens by name substring")
    parser.add_argument("--created-before", type=str, help="Filter tokens created before (YYYY-MM-DD)")
    parser.add_argument("--created-after", type=str, help="Filter tokens created after (YYYY-MM-DD)")
    args = parser.parse_args()

    client = GitLabAPIClient()

    display_section("External Users", client.get_external_users(search=args.search_user))
    display_section("Project Access Tokens", client.get_project_tokens(args.project_id))
    display_section("CI/CD Pipelines", client.get_pipelines(args.project_id, ref=args.ref, status=args.status))
    display_section("Webhooks", client.get_webhooks(args.project_id))
    display_section("Instance Audit Logs", client.get_instance_audit_logs())

    if args.check_token_expiry:
        display_section("Tokens Nearing Expiry", client.check_token_expiry(
            args.project_id,
            token_name=args.token_name,
            created_before=args.created_before,
            created_after=args.created_after
        ))
