gcloud functions deploy sw-cf-gcs-ps-bq \
  --gen2 \
  --runtime=python311 \
  --region=us-west1 \
  --source=src \
  --entry-point=bq_load_from_gcs \
  --memory 16384MB \
  --timeout 540s  \
  --trigger-topic sw-df-cf-bq-ingest