from google.cloud import bigquery, pubsub_v1
import logging
from google.api_core.exceptions import NotFound, Forbidden
import base64
import json
import os

def bq_load_from_gcs(event, context):
    print(f'Received event: {event}')  
    logging.info(f'Received event: {event}')

    try:
        pubsub_message = base64.b64decode(event['data']).decode('utf-8')
        message_dict = json.loads(pubsub_message)

        project_id = message_dict.get('project_id')
        original_date = message_dict.get('original_date')
        dataset_id = message_dict.get('dataset_id')
        table_id = message_dict.get('table_id')
        destination_bucket = message_dict.get('destination_bucket')

        gcs_uri = f'gs://{destination_bucket}/{original_date}/{table_id}/*.csv'
        bigquery_uri = f'{project_id}:{dataset_id}.{table_id}'

        client = bigquery.Client(project=project_id)
        publisher = pubsub_v1.PublisherClient()
        pubsub_topic = os.getenv('PUBSUB_TOPIC')
        topic_path = publisher.topic_path(project_id, pubsub_topic)

        # Check if the dataset exists and create if it doesn't
        try:
            client.get_dataset(dataset_id)  # Make an API request.
        except NotFound:
            dataset = bigquery.Dataset(client.dataset(dataset_id))
            client.create_dataset(dataset)
            print(f'Created dataset {project_id}.{dataset_id}')

        table_ref = client.dataset(dataset_id).table(table_id)

        # Check if the table exists and create if it doesn't
        try:
            client.get_table(table_ref)  # Make an API request.
        except NotFound:
            schema=[
                bigquery.SchemaField("datetime", "STRING"),
                bigquery.SchemaField("measurement_name", "STRING"),
                bigquery.SchemaField("millis", "STRING"),
                bigquery.SchemaField("measurement_value", "STRING"),
                bigquery.SchemaField("measurement_status", "STRING"),
            ]
            table = bigquery.Table(table_ref, schema=schema)
            table = client.create_table(table)
            print(f'Created table {table.project}.{table.dataset_id}.{table.table_id}')

        # Now we can proceed with the loading job.
        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.CSV,
            schema=[
                bigquery.SchemaField("datetime", "STRING"),
                bigquery.SchemaField("measurement_name", "STRING"),
                bigquery.SchemaField("millis", "STRING"),
                bigquery.SchemaField("measurement_value", "STRING"),
                bigquery.SchemaField("measurement_status", "STRING"),
            ],
        )
        
        load_job = client.load_table_from_uri(gcs_uri, table_ref, job_config=job_config)
        
        print(f'Started job {load_job.job_id}')
        
        load_job.result()  # Waits for the job to complete.
        
        destination_table = client.get_table(table_ref)
        print(f'Loaded {destination_table.num_rows} rows to {bigquery_uri}.')

        message = {
            'project_id': project_id,
            'dataset_id': dataset_id,
            'table_id' : table_id,
        }
        
        try:
            publish_message = publisher.publish(topic_path, json.dumps(message).encode('utf-8'))
            publish_message.result()
        except Exception as e:
            print(f'An error occurred when trying to publish message: {str(e)}')
            raise

    except Forbidden as e:
        print(f'Error occurred: {str(e)}. Please check the Cloud Function has necessary permissions.')
        raise