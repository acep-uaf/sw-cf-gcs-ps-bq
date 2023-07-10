# SW-CF-GCS-PS-BQ Cloud Function and Associated Workflow

The `sw-cf-gcs-ps-bq` is a Cloud Function designed to ingest data from a Google Cloud Storage (GCS) bucket, load it into a BigQuery table, and then publish a message to a Pub/Sub topic. This function is triggered by a Google Cloud Workflow named `sw-cw-cf-gcs-bq`.

## Cloud Function

### Description

The Cloud Function `sw-cf-gcs-ps-bq` is written in Python and uses the Google Cloud `bigquery` and `pubsub` libraries to interact with BigQuery and Pub/Sub. The function is triggered by a Pub/Sub topic and is responsible for ingesting data from a GCS bucket into a BigQuery table, and then publishing a message to another Pub/Sub topic.

### Deployment

Deploy this Cloud Function by running the `eiedeploy.sh` shell script:

\```bash
./eiedeploy.sh
\```

This script wraps the following `gcloud` command:

\```bash
gcloud functions deploy sw-cf-gcs-ps-bq \
  --gen2 \
  --runtime=python311 \
  --region=us-west1 \
  --source=src \
  --entry-point=bq_load_from_gcs \
  --memory 16384MB \
  --timeout 540s  \
  --trigger-topic sw-df-cf-bq-ingest
\```

### Dependencies

The Cloud Function's dependencies are listed in the `requirements.txt` file and include the `google-cloud-pubsub`, `google-cloud-storage`, and `google-cloud-bigquery` packages.

## Cloud Workflow

The `sw-cw-cf-gcs-bq` workflow is responsible for decoding the Pub/Sub message and making a HTTP POST request to the Cloud Function URL. This workflow is triggered by an Eventarc trigger, which is set up to activate the workflow upon the publishing of a message on a Pub/Sub topic.

### Deployment

The deployment of the workflow and its associated components is managed by three shell scripts:

1. `cw-deploy.sh`: This script deploys the workflow using Google Cloud Workflows. The workflow is defined in the `cw.json` file and is deployed to a specific location (`us-west1` in this case) with a specified service account.

2. `cw-subscription.sh`: This script creates a Pub/Sub subscription which will receive messages from a specified topic and forward them to the workflow.

3. `cw-trigger.sh`: This script sets up an Eventarc trigger that will activate the workflow upon the publishing of a message on a Pub/Sub topic.

The order in which to run these scripts is as follows:

1. `cw-deploy.sh`
2. `cw-subscription.sh`
3. `cw-trigger.sh`

This order ensures that the workflow is deployed before it is referenced by the other scripts, and that the Pub/Sub subscription is created before the Eventarc trigger is set up. Before running these scripts, make sure that the Cloud Function is already deployed, as it is referenced in the workflow.
