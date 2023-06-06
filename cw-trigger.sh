gcloud eventarc triggers create sw-cw-cf-gcs-bq-trigger \
  --destination-workflow=sw-cw-cf-gcs-bq \
  --destination-workflow-location=us-west1 \
  --event-filters="type=google.cloud.pubsub.topic.v1.messagePublished" \
  --service-account=untar-ingest@acep-ext-eielson-2021.iam.gserviceaccount.com \
  --location=us-west1