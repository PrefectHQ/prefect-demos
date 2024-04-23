from prefect_kubernetes.jobs import KubernetesJob, KubernetesJobRun


from kubernetes.client import (
    V1Job,
    V1ObjectMeta,
    V1JobSpec,
    V1PodTemplateSpec,
    V1PodSpec,
    V1Container,
)
from kubernetes.client.models import V1DeleteOptions

metadata = V1ObjectMeta(name="r-script-job")
container = V1Container(
    name="r-script-container",
    image="myrscriptimage:latest",  # Use the correct path to your Docker image
    image_pull_policy="Always",
)
template = V1PodTemplateSpec(
    metadata=V1ObjectMeta(labels={"app": "r-script"}),
    spec=V1PodSpec(restart_policy="Never", containers=[container]),
)
spec = V1JobSpec(template=template, backoff_limit=4)
v1_job_model = V1Job(api_version="batch/v1", kind="Job", metadata=metadata, spec=spec)

# Serialize the v1_job_model to a dictionary
v1_job_dict = v1_job_model.to_dict()

# Assuming KubernetesJob expects a dictionary for the v1_job parameter
r_script_kubernetes_job = KubernetesJob(
    v1_job=v1_job_dict,  # Pass the serialized job model as a dictionary
    name="r-script-job",
    namespace="default",  # Adjust as necessary
    credentials={},  # Provide the necessary credentials
)
