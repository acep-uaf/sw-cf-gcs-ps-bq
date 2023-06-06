gcloud workflows deploy sw-cw-cf-gcs-bq \
  --source=cw.json \
  --service-account=untar-ingest@acep-ext-eielson-2021.iam.gserviceaccount.com \
  --location=us-west1

