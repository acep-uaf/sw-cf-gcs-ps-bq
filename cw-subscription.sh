gcloud pubsub subscriptions create sw-cw-cf-gcs-bq-subscription \
  --topic=sw-df-cf-bq-ingest \
  --push-endpoint="https://workflowexecutions.googleapis.com/v1/projects/acep-ext-eielson-2021/locations/us-west1/workflows/sw-cw-cf-gcs-bq/executions" \
  --push-auth-service-account=untar-ingest@acep-ext-eielson-2021.iam.gserviceaccount.com
