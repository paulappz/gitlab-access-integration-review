# GitLab Access Audit Tool  
A Python and Postman-based tool to audit third-party access to GitLab.  

## Features  
- List users with external identities (OAuth/SAML).  
- Retrieve project access tokens and audit logs.  
- Pagination support for large datasets.  

## Setup  
1. **Clone the repository**:  
   ```bash
   git clone https://github.com/your-repo/gitlab-access-audit.git
   cd gitlab-access-audit
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
```bash
python api/gitlab_client.py
```

### Postman:
- Import `api/postman/GitLab_Collection.json` and `GitLab_Environment.json` into Postman.
- Set environment variables in Postman:
  - `GITLAB_URL`: Your GitLab instance URL.
  - `PRIVATE_TOKEN`: Your Personal Access Token.

## Endpoints Covered
| Endpoint                          | Description               |
|------------------------------------|---------------------------|
| `/users`                           | List external users       |
| `/projects/:id/access_tokens`     | List project tokens       |
| `/groups/:id/audit_events`        | Fetch audit logs          |