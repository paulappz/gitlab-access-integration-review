# GitLab Access & Integration Review  
**Objective**: Provide a structured overview of third-party access/integration methods, API usage guidelines, and security best practices.  

---

## 1. Overview  
### Authentication & Access Methods  
- **External Authentication**:  
  - **OAuth 2.0**: Tokens passed via `access_token` or `Authorization` header ([GitLab OAuth Docs](https://docs.gitlab.com/ee/api/oauth2.html)).  
  - **LDAP/Active Directory**: Centralized user management ([LDAP Integration Guide](https://docs.gitlab.com/omnibus/settings/ldap.html)).  
  - **SAML SSO**: Enterprise-grade SSO with IdPs like Okta or Azure AD ([SAML Configuration](https://docs.gitlab.com/ee/user/group/saml_sso/)).  
  - **Personal Access Tokens (PATs)**: Used for API/Git over HTTPS.  
  - **2FA Enforcement**: Mandatory for high-security environments.  

- **Access Control**:  
  - **Instance Level**: Global settings (e.g., enforced 2FA).  
  - **Group Level**: Roles (Guest, Developer, Maintainer) with cascading permissions.  
  - **Project Level**: Granular control over repositories and CI/CD.  

- **Programmatic Access**:  
  - **API Tokens**: Personal, project, or group-level tokens.  
  - **CI/CD Automation**: Trigger pipelines via API calls or webhooks.  

### Integrations & Extensions  
- **Key Integrations**:  
  - **Jenkins**: CI/CD pipeline triggers ([Jenkins Integration](https://docs.gitlab.com/ee/integration/jenkins.html)).  
  - **Slack**: Real-time notifications for merge requests/pipelines.  
  - **Kubernetes**: Auto-deploy to clusters via `.gitlab-ci.yml`.  

- **Permission Models**:  
  - **OAuth Scopes**: Limit third-party app permissions (e.g., `read_user` or `api`).  
  - **Webhooks**: Secured with secret tokens to validate payloads.  
