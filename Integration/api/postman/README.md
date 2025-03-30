# GitLab Access Audit

This project provides a Postman collection and Python script for auditing third-party (external) access to a GitLab instance.

## 🔧 Environment Setup

1. **Set Environment Variables in Postman**

Create a Postman environment and define the following variables:

| Variable        | Description                                                |
|----------------|------------------------------------------------------------|
| `GITLAB_URL`   | Your GitLab instance URL (e.g., http://your-gitlab.com)    |
| `PRIVATE_TOKEN`| GitLab personal access token with `read_api` and `read_user` scopes |
| `PROJECT_ID`   | The project ID you want to audit                           |
| `GROUP_ID`     | The group ID you want to audit                             |

## 📦 Import and Run the Collection

1. Open Postman.
2. Click **Import** > **File** and upload the `gitlab_collection.json` file.
3. Select the created environment.
4. Run each request or use the **Collection Runner** to run them all.

## ✅ Test Scripts

Each request includes a test script to verify a `200 OK` response. You can add more assertions depending on your use case, e.g.:

```javascript
pm.test("Response is JSON", function () {
    pm.response.to.be.withBody;
    pm.response.to.be.json;
});

pm.test("Contains expected fields", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.be.an("array");
});
```

## 🐍 Optional Python Script

This repo may include a Python script (`gitlab_client.py`) for auditing via CLI using the GitLab API. Set up a `.env` file with:

```
GITLAB_URL=http://your-gitlab.com
PRIVATE_TOKEN=your_access_token
```

Then run:

```bash
python gitlab_client.py --project-id <PROJECT_ID> --group-id <GROUP_ID>
```

## 📤 Export Postman Collection

To re-export the collection (after adding requests/tests):

1. Click on the collection name.
2. Click **Export**.
3. Choose **Collection v2.1** format.
4. Save the file to include in your Git repo.

---

Created for GitLab audit integration automation.
