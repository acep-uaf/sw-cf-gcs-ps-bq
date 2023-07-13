# SW-CF-GCS-PS-BQ Cloud Function and Associated Workflow

The `sw-cf-gcs-ps-bq` is a Cloud Function designed to ingest data from a Google Cloud Storage (GCS) bucket, load it into a BigQuery table, and then publish a message to a Pub/Sub topic.

## Cloud Function

### Description

The gen 2 Cloud Function `bq_load_from_gcs` is a Python function that leverages the `google.cloud.bigquery` and `google.cloud.pubsub_v1` libraries to interact with Google's BigQuery and Pub/Sub services. The function is initiated by an event from a Pub/Sub topic.

Upon receiving the event, the function decodes the base64-encoded data from the event payload and loads the resulting JSON string into a Python dictionary. From this dictionary, it fetches crucial information such as the `project_id`, `original_date`, `dataset_id`, `table_id`, and `destination_bucket`.

The function then constructs a Google Cloud Storage URI pointing to the source CSV files in the bucket and the BigQuery URI of the destination table where the data is to be loaded. It sets up a BigQuery client with the specified `project_id` and a Pub/Sub publisher.

The function checks if the specified dataset and table exist in the BigQuery project. If they do not exist, the function will create them, setting up a specific schema for the new table, which includes fields like `datetime`, `measurement_name`, `millis`, `measurement_value`, and `measurement_status`.

After ensuring the dataset and table's existence, the function initiates a BigQuery load job to import the CSV data from the Cloud Storage bucket to the BigQuery table. The function waits for the completion of this job, then retrieves the final table to log the number of rows loaded.

The function then prepares a new message that includes the `project_id`, `dataset_id`, and `table_id` and publishes this message to a specific Pub/Sub topic (`sw-cf-bq-pp-dt-rs`). This event signifies that the loading job has finished successfully, potentially triggering further downstream processes.

In the case of a `Forbidden` exception or any issues with publishing the Pub/Sub message, the function logs the error message and raises the exception.

In summary, the `bq_load_from_gcs` function serves as a data pipeline connector that transfers data from GCS to BigQuery and triggers subsequent processes upon successful data load, effectively automating and managing the flow of data across different Google Cloud services.
.

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
