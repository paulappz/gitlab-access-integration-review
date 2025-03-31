# GitLab Access Audit Tool  
A Python and Postman-based tool to audit third-party access to GitLab.  

## Features  
- List users with external identities (OAuth/SAML).
- Retrieve project access tokens, CI/CD pipelines, webhooks, and audit logs.
- Filter pipelines by ref and status.
- Monitor project access tokens nearing expiry.
- Pagination support for large datasets.
- Postman collection with variable support for GitLab API testing.
- Pytest test suite for unit testing core functionalities.

## Setup  
1. **Clone the repository**:  
   ```bash
   git clone https://github.com/paulappz/gitlab-access-integration-review.git
   cd gitlab-access-integration-review/integration
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**:
   - Copy `config/.env.example` to `.env`.
   - Update `.env` with your GitLab URL and access token.

## Usage

### Python Script:
Run the audit using:
```bash
python api/gitlab_client.py --project-id 2 --group-id 4 --search-user "external" --ref main --status failed --check-token-expiry
```

**Available CLI Options:**

| Flag | Description |
|------|-------------|
| `--project-id` | **Required**. ID of the GitLab project to audit |
| `--group-id` | Optional. Group ID if auditing within a group context |
| `--search-user` | Filter external users by name or email |
| `--ref` | Filter pipelines by branch/ref (e.g., `main`) |
| `--status` | Filter pipelines by status (`success`, `failed`, etc.) |
| `--check-token-expiry` | Display tokens nearing expiry in 30 days |

<details>
<summary> View sample output  (click to expand)</summary>
<center>
  <img  src='img/api.png'  border='1px'  />
</center>

<center>
  <img  src='img/api_v2.png'  border='1px'  />
</center>

<center>
  <img  src='img/api_v2+.png'  border='1px'  />
</center>
</details>

### Postman:
- Import `api/postman/gitlab_collection.json` into Postman.
- Set environment variables in Postman:
  - `GITLAB_URL`: Your GitLab instance URL.
  - `PRIVATE_TOKEN`: Your Personal Access Token.
  - `PROJECT_ID`: Project ID to audit.
  - `GROUP_ID`: Group ID to audit.
- Run collection in Postman:

<details>
<summary> View sample output  (click to expand)</summary>
<center>
  <img  src='img/postman.png'  border='1px'  />
</center>

<center>
  <img  src='img/postman_v2.png'  border='1px'  />
</center>
</details>

## Endpoints Covered
| Endpoint                               | Description                          |
|----------------------------------------|--------------------------------------|
| `/users?externals=true`                | List external users                  |
| `/projects/:id/access_tokens`          | List project tokens                  |
| `/projects/:id/pipelines`              | List project CI/CD pipelines         |
| `/projects/:id/hooks`                  | List project webhooks                |
| `/audit_events`                        | Fetch instance audit logs (Premium)  |

## Testing
Run the test suite using:
```bash
PYTHONPATH=. pytest tests/test_gitlab_client.py -v
```

<details>
<summary> View sample output  (click to expand)</summary>
<center>
  <img  src='img/test.png'  border='1px'  />
</center>

<center>
  <img  src='img/test_v2.png'  border='1px'  />
</center>

</details>

## Notes
- Audit logs (`/audit_events`) require GitLab Premium or higher.
- Use the admin token with `read_api` and `read_user` scopes.
- Pipeline and token filters help narrow down audit results for large-scale use cases.