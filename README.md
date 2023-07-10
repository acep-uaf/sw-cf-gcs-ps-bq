# SW-CF-GCS-PS-BQ Cloud Function and Associated Workflow

The `sw-cf-gcs-ps-bq` is a Cloud Function designed to ingest data from a Google Cloud Storage (GCS) bucket, load it into a BigQuery table, and then publish a message to a Pub/Sub topic. This function is triggered by a Google Cloud Workflow named `sw-cw-cf-gcs-bq`.

## Cloud Function

### Description