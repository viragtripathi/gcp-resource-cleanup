#!/bin/bash
set -e

if [[ -z "$1" ]]; then
  echo "Usage: ./deploy.sh <gcp-project-id>"
  exit 1
fi

PROJECT_ID=$1
TOPIC="cleanup-trigger"
FUNCTION_NAME="cleanup_resources"

echo "➡️ Creating Pub/Sub topic (if not exists)..."
gcloud pubsub topics create $TOPIC --project=$PROJECT_ID || true

echo "➡️ Deploying Cloud Function..."
gcloud functions deploy $FUNCTION_NAME \
  --runtime python310 \
  --trigger-topic $TOPIC \
  --entry-point cleanup_resources \
  --timeout=540s \
  --memory=512MB \
  --set-env-vars "CONFIG_PATH=config.json" \
  --project=$PROJECT_ID

echo "✅ Deployment complete."

