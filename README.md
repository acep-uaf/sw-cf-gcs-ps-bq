# SW-CF-GCS-PS-BQ Cloud Function and Associated Workflow

The `sw-cf-gcs-ps-bq` is a Cloud Function designed to ingest data from a Google Cloud Storage (GCS) bucket, load it into a BigQuery table, and then publish a message to a Pub/Sub topic.

## Cloud Function

### Description

The gen 2 Cloud Function `sw-cf-gcs-ps-bq` is written in Python and uses the Google Cloud `bigquery` and `pubsub` libraries to interact with BigQuery and Pub/Sub. The function is triggered by a Pub/Sub topic and is responsible for ingesting data from a GCS bucket into a BigQuery table, and then publishing a message to another Pub/Sub topic.

### Deployment

Deploy this Cloud Function by running the `eiedeploy.sh` shell script:

```bash
./eiedeploy.sh
```


This script wraps the following `gcloud` command:

```bash
gcloud functions deploy sw-cf-gcs-ps-bq \
  --gen2 \
  --runtime=python311 \
  --region=us-west1 \
  --source=src \
  --entry-point=bq_load_from_gcs \
  --memory 16384MB \
  --timeout 540s  \
  --trigger-topic sw-df-cf-bq-ingest
```


### Dependencies

The Cloud Function's dependencies are listed in the `requirements.txt` file and include the `google-cloud-pubsub`, `google-cloud-storage`, and `google-cloud-bigquery` packages.
