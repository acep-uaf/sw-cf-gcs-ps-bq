# SW-CF-GCS-PS-BQ Cloud Function
<br>

Introducing the `sw-cf-gcs-ps-bq` repository—a key element of the ACEP SW Data Pipeline. This component is tailored to initiate the ETL jobs, particularly the BigQuery ingestion once the unpacked data is stored in the secondary GCP bucket.

For an in-depth understanding of the entire data pipeline and this repository's role, please consult the [ACEP SW Data Pipeline Overview](https://github.com/acep-uaf/sw-stack) repository.

The `sw-cf-gcs-ps-bq` is a Cloud Function designed to ingest data from a Google Cloud Storage (GCS) bucket, load it into a BigQuery table, and then publish a message to a Pub/Sub topic.

## Cloud Function

### Description

The gen 2 Cloud Function `bq_load_from_gcs` is a Python function that leverages the `google.cloud.bigquery`, `google-cloud-storage` and `google.cloud.pubsub_v1` libraries to interact with Google's BigQuery and Pub/Sub services. The function is initiated by an event from a Pub/Sub topic.

Upon receiving the event, the function decodes the base64-encoded data from the event payload and loads the resulting JSON string into a Python dictionary. From this dictionary, it fetches crucial information such as the `project_id`, `original_date`, `dataset_id`, `table_id`, and `destination_bucket`.

The function then constructs a Google Cloud Storage URI pointing to the source CSV files in the bucket and the BigQuery URI of the destination table where the data is to be loaded. It sets up a BigQuery client with the specified `project_id` and a Pub/Sub publisher.

The function checks if the specified dataset and table exist in the BigQuery project. If they do not exist, the function will create them, setting up a specific schema for the new table, which includes fields like `datetime`, `measurement_name`, `millis`, `measurement_value`, and `measurement_status`.

After ensuring the dataset and table's existence, the function initiates a BigQuery load job to import the CSV data from the Cloud Storage bucket to the BigQuery table. The function waits for the completion of this job, then retrieves the final table to log the number of rows loaded.

The function then prepares a new message that includes the `project_id`, `dataset_id`, and `table_id` and publishes this message to a specific Pub/Sub topic `PUBSUB_TOPIC`. This event signifies that the loading job has finished successfully, potentially triggering further downstream processes.

In the case of a `Forbidden` exception or any issues with publishing the Pub/Sub message, the function logs the error message and raises the exception.

In summary, the `bq_load_from_gcs` function serves as a data pipeline connector that transfers data from GCS to BigQuery and triggers subsequent processes upon successful data load, effectively automating and managing the flow of data across different Google Cloud services.

### Deployment

Deploy the Cloud Function with the provided shell script:

```bash
./eiedeploy.sh
```


This script wraps the following `gcloud` command:

```bash
#!/bin/bash

# Source the .env file
source eiedeploy.env

# Deploy the function
gcloud functions deploy sw-cf-gcs-ps-bq \
  --$GEN2 \
  --runtime=$RUNTIME \
  --region=$REGION \
  --service-account=$SERVICE_ACCOUNT \
  --source=$SOURCE \
  --entry-point=$ENTRY_POINT \
  --memory=$MEMORY \
  --timeout=$TIMEOUT \
  --trigger-topic=$TRIGGER_TOPIC \
  --set-env-vars PUBSUB_TOPIC=$PUBSUB_TOPIC
```
 ### .env File Configuration

Before deploying the Cloud Function, ensure that the `eiedeploy.env` file contains the necessary environment variables, as the deployment script sources this file. This file should define values for:

```bash
  GEN2=<value>
  RUNTIME=<value>
  REGION=<value>
  SERVICE_ACCOUNT=<value>
  SOURCE=<value>
  ENTRY_POINT=<value>
  MEMORY=<value>
  TIMEOUT=<value>
  TRIGGER_TOPIC=<value>
  PUBSUB_TOPIC=<value>
 ```
 Replace `<value>` with the appropriate values for your deployment.

 ### Environment Variable Descriptions
 
 Below are descriptions for each environment variable used in the deployment script:
 
 - **GEN2**=`<value>`:
   - Description: Specifies the generation of the Cloud Function to deploy.  For example: `gen2` when you intend to deploy a second generation Google Cloud Function.
 
 - **RUNTIME**=`<value>`:
   - Description: Specifies the runtime environment in which the Cloud Function executes. For example: `python311` for Python 3.11.
 
 - **REGION**=`<value>`:
   - Description: The Google Cloud region where the Cloud Function will be deployed and run. Example values are `us-west1`, `europe-west1`, etc.
 
 - **SERVICE_ACCOUNT**=`<value>`:
   - Description: The service account under which the Cloud Function will run. This defines the permissions that the Cloud Function has at deployment.
 
 - **SOURCE**=`<value>`:
   - Description: Path to the source code of the Cloud Function. Typically, this points to a directory containing all the necessary files for the function.
 
 - **ENTRY_POINT**=`<value>`:
   - Description: Specifies the name of the function or method within the source code to be executed when the Cloud Function is triggered.
 
 - **MEMORY**=`<value>`:
   - Description: The amount of memory to allocate for the Cloud Function. This is denoted in megabytes, e.g., `16384MB`.
 
 - **TIMEOUT**=`<value>`:
   - Description: The maximum duration the Cloud Function is allowed to run before it is terminated. Expressed in seconds, e.g., `540s`.
 
 - **TRIGGER_TOPIC**=`<value>`:
   - Description: The Google Cloud topic under which the Cloud Function is subscribed.
 
 - **PUBSUB_TOPIC**=`<value>`:
   - Description: The name of the Pub/Sub topic to which the Cloud Function publishes messages.
 
 Set each `<value>` in the `eiedeploy.env` file appropriately before deploying the Cloud Function. **Note:** For security reasons, do not cheeck the `eiedeploy.env` with values set into a public repository such as github.

### Dependencies

The Cloud Function's dependencies are listed in the `requirements.txt` file and include:
- `google-cloud-pubsub` 
- `google-cloud-storage` 
- `google-cloud-bigquery`

### Conclusion

---

The `sw-cf-gcs-ps-bq` repository stands as a cornerstone of the [ACEP SW Data Pipeline](https://github.com/acep-uaf/sw-stack). This Cloud Function is meticulously crafted to foster interaction with Google Cloud Storage (GCS), BigQuery, and Pub/Sub, facilitating an automated process of ingesting data into BigQuery once it's available in a GCS bucket.

With this repository, the synergy between cloud storage, event-driven computing, and data warehousing on the Google Cloud Platform is vividly demonstrated. As data becomes available or is modified in the bucket, `sw-cf-gcs-ps-bq` stands vigilant, swiftly initiating ETL jobs and signaling through Pub/Sub. This ensures that any connected services or systems can respond immediately, augmenting the automation and responsiveness of the entire data pipeline.

We invite the open-source community to delve deep into this repository, appreciate its intricacies, and contribute towards refining it further. For comprehensive licensing details, please see the [LICENSE](https://github.com/acep-uaf/sw-cf-gcs-ps-bq/blob/main/LICENSE) file situated in the main directory of the repository.

Your engagement with this solution is valued, and we trust that it will substantially enhance your data processing endeavors within the GCP framework.

---
