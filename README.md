# GCP Resource Cleanup Automation

This project automates the cleanup of stale GCP resources (e.g. GCE snapshots, GCS objects, Cloud SQL backups) using:

- **Cloud Functions** (to run cleanup logic)
- **Pub/Sub** (to trigger the function)
- **Cloud Scheduler** (to schedule periodic cleanup)
- **Virtualenv (venv)** for Python dependency isolation

---

## 🚀 Quickstart

### 1. Clone the Repo

```bash
git clone https://github.com/viragtripathi/gcp-resource-cleanup.git
cd gcp-resource-cleanup
````

### 2. Create and Activate Python Virtual Environment

```bash
./setup.sh
source venv/bin/activate
```

### 3. Configure the Cleanup Behavior

Edit `config.json` and replace `"your-gcp-project-id"` with your actual project ID.

```json
{
  "project_id": "your-gcp-project-id",
  "retention_days": 30,
  "resources": {
    "gce_snapshots": true,
    "gcs_buckets": true,
    "cloudsql_backups": true
  }
}
```

---

## 🛠️ Deploy the Cloud Function

```bash
./deploy.sh your-gcp-project-id
```

This deploys the function and sets up a Pub/Sub topic to trigger it.

---

## ⏰ Schedule Cleanup via Cloud Scheduler

```bash
gcloud scheduler jobs create pubsub daily-cleanup-job \
  --schedule="0 3 * * *" \
  --time-zone="UTC" \
  --topic=cleanup-trigger \
  --message-body="{}" \
  --project=your-gcp-project-id
```

---

## 🧪 Local Testing (Optional)

You can test logic by running:

```bash
source venv/bin/activate
python main.py
```

> You can adapt `main.py` to allow direct invocation with test config for local runs.

---

## 🔐 IAM Permissions Required

Ensure your Cloud Function's service account has:

* `roles/compute.storageAdmin` (GCE snapshots)
* `roles/storage.admin` (GCS)
* `roles/cloudsql.admin` (Cloud SQL backups)

---

## 📦 Structure

| File               | Purpose                                            |
|--------------------|----------------------------------------------------|
| `main.py`          | Resource cleanup logic                             |
| `config.json`      | Configurable resource types and age thresholds     |
| `requirements.txt` | Python packages required                           |
| `setup.sh`         | Creates and activates a Python virtual environment |
| `deploy.sh`        | Deploys Cloud Function using gcloud                |

---

## 📌 Supported Resources

* ✅ GCE Snapshots
* ✅ GCS Objects
* ✅ Cloud SQL Backups

More can be added by extending `main.py`.
