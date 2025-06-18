import json
from datetime import datetime, timezone, timedelta
from googleapiclient import discovery
from google.cloud import storage

def cleanup_snapshots(project_id, cutoff):
    compute = discovery.build('compute', 'v1')
    result = compute.snapshots().list(project=project_id).execute()
    for snap in result.get('items', []):
        created = datetime.strptime(snap['creationTimestamp'], "%Y-%m-%dT%H:%M:%S.%f%z")
        if created < cutoff:
            print(f"Deleting GCE snapshot: {snap['name']}")
            compute.snapshots().delete(project=project_id, snapshot=snap['name']).execute()

def cleanup_gcs_objects(project_id, cutoff):
    client = storage.Client(project=project_id)
    for bucket in client.list_buckets():
        for blob in client.bucket(bucket.name).list_blobs():
            if blob.time_created < cutoff:
                print(f"Deleting GCS object: gs://{bucket.name}/{blob.name}")
                blob.delete()

def cleanup_cloudsql_backups(project_id, cutoff):
    sql = discovery.build('sqladmin', 'v1beta4')
    instances = sql.instances().list(project=project_id).execute().get('items', [])
    for inst in instances:
        backups = sql.backupRuns().list(project=project_id, instance=inst['name']).execute().get('items', [])
        for backup in backups:
            end_time = datetime.strptime(backup['endTime'], "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc)
            if end_time < cutoff:
                print(f"Deleting Cloud SQL backup: {backup['id']} from {inst['name']}")
                sql.backupRuns().delete(project=project_id, instance=inst['name'], id=backup['id']).execute()

def cleanup_resources(event, context=None):
    with open("config.json") as f:
        cfg = json.load(f)

    project_id = cfg["project_id"]
    days = cfg.get("retention_days", 30)
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    res = cfg["resources"]

    if res.get("gce_snapshots", False):
        cleanup_snapshots(project_id, cutoff)
    if res.get("gcs_buckets", False):
        cleanup_gcs_objects(project_id, cutoff)
    if res.get("cloudsql_backups", False):
        cleanup_cloudsql_backups(project_id, cutoff)
