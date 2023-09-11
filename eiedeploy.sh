#!/bin/bash

# Source the .env file
source eiedeploy.env

# Deploy the function
gcloud functions deploy sw-cf-gcs-ps-bq \
  --$GEN2 \
  --runtime=$RUNTIME \
  --region=$REGION \
  --source=$SOURCE \
  --entry-point=$ENTRY_POINT \
  --memory=$MEMORY \
  --timeout=$TIMEOUT \
  --trigger-topic=$TRIGGER_TOPIC \
  --set-env-vars PUBSUB_TOPIC=$PUBSUB_TOPIC