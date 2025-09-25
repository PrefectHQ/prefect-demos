import functions_framework
from prefect.events import emit_event

# Triggered by a change in a storage bucket
@functions_framework.cloud_event
def pipe_to_prefect(cloud_event):
    data = cloud_event.data

    event_id = cloud_event["id"]
    event_type = cloud_event["type"]

    bucket = data["bucket"]
    name = data["name"]
    metageneration = data["metageneration"]
    timeCreated = data["timeCreated"]
    updated = data["updated"]

    event = emit_event(
      event="gcs.processed.object.created",
      resource={
        "prefect.resource.id": event_id,
        "gcs_bucket": bucket,
        "key": name,
        "created": timeCreated,
        "updated": updated
      }
    )

    print(f"Event ID: {event_id}")
    print(f"Event type: {event_type}")
    print(f"Bucket: {bucket}")
    print(f"File: {name}")
    print(f"Metageneration: {metageneration}")
    print(f"Created: {timeCreated}")
    print(f"Updated: {updated}")

