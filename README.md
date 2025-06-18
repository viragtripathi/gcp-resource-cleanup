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

---

## 🔐 Prerequisites: GCloud CLI & Auth Setup

Before deploying this automation, ensure the following tools and access are set up:

### ✅ 1. Install GCloud CLI

Follow the official instructions here:
👉 [https://cloud.google.com/sdk/docs/install](https://cloud.google.com/sdk/docs/install)

Then verify installation:

```bash
gcloud version
```

### ✅ 2. Authenticate to GCP

If not already authenticated:

```bash
gcloud auth login
```

Then set your default project:

```bash
gcloud config set project your-gcp-project-id
```

### ✅ 3. Enable Required APIs

This project requires these GCP APIs:

```bash
gcloud services enable \
  cloudfunctions.googleapis.com \
  pubsub.googleapis.com \
  cloudscheduler.googleapis.com \
  compute.googleapis.com \
  storage.googleapis.com \
  sqladmin.googleapis.com
```

### ✅ 4. Permissions Required

Ensure your user or Cloud Function **service account** has the following IAM roles:

| Role                             | Purpose                    |
|----------------------------------|----------------------------|
| `roles/compute.storageAdmin`     | Manage GCE snapshots       |
| `roles/storage.admin`            | Delete GCS objects         |
| `roles/cloudsql.admin`           | Cleanup Cloud SQL backups  |
| `roles/pubsub.publisher`         | Publish Scheduler messages |
| `roles/cloudfunctions.developer` | Deploy functions           |

You can grant these roles via IAM in the Google Cloud Console or using CLI:

```bash
gcloud projects add-iam-policy-binding your-gcp-project-id \
  --member="user:your.email@example.com" \
  --role="roles/compute.storageAdmin"
```

(Repeat for other roles as needed.)
