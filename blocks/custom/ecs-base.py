"""
pip install prefect -U
pip install prefect-aws
prefect block register -m prefect_aws.ecs
"""
from prefect_aws.ecs import ECSTask
from prefect.filesystems import S3

s3_storage = S3(bucket_path="se-demo-flow-code-store")

basic_ecs = ECSTask(
    cpu="256",
    memory="512",
    cluster="prefect-agent-prod-fargate-prefect-agent",
    stream_output=True,
    execution_role_arn="arn:aws:iam::455346737763:role/prefect-agent-execution-role-prod-fargate-prefect-agent",
    task_role_arn="arn:aws:iam::123456789:role/dataflowops_ecs_task_role",
)


# ecs = ECSTask(
#     image="annaprefect/prefect-s3:latest",  # example image
# cpu="256",
# memory="512",
# stream_output=True,
#     configure_cloudwatch_logs=True,
#     cluster="prefect",
#     execution_role_arn="arn:aws:iam::123456789:role/dataflowops_ecs_execution_role",
#     task_role_arn="arn:aws:iam::123456789:role/dataflowops_ecs_task_role",
#     task_definition={
#         "taskDefinitionArn": "arn:aws:ecs:us-east-2:455346737763:task-definition/prefect-agent-prod-fargate-prefect-agent:2",
#         "containerDefinitions": [
#             {
#                 "name": "prefect-agent-prod-fargate-prefect-agent",
#                 "image": "prefecthq/prefect:2-python3.10",
#                 "cpu": 1024,
#                 "memory": 2048,
#                 "command": ["prefect", "agent", "start", "-q", "prod-ecs"],
#                 "environment": [
#                     {
#                         "name": "PREFECT_API_URL",
#                         "value": "https://api.prefect.cloud/api/accounts/0ff44498-d380-4d7b-bd68-9b52da03823f/workspaces/bb3005b9-99c6-4289-802b-6cfbfcffc5c0",
#                     },
#                     {"name": "EXTRA_PIP_PACKAGES", "value": "prefect-aws s3fs"},
#                 ],
#                 "mountPoints": [],
#                 "volumesFrom": [],
#                 "secrets": [
#                     {
#                         "name": "PREFECT_API_KEY",
#                         "valueFrom": "arn:aws:secretsmanager:us-east-2:455346737763:secret:prefect-api-key-prod-fargate-prefect-agent-Yn8oOX",
#                     }
#                 ],
#                 "logConfiguration": {
#                     "logDriver": "awslogs",
#                     "options": {
#                         "awslogs-group": "prefect-agent-log-group-prod-fargate-prefect-agent",
#                         "awslogs-region": "us-east-2",
#                         "awslogs-stream-prefix": "prefect-agent-prod-fargate-prefect-agent",
#                     },
#                 },
#             }
#         ],
#         "family": "prefect-agent-prod-fargate-prefect-agent",
#         "executionRoleArn": "arn:aws:iam::455346737763:role/prefect-agent-execution-role-prod-fargate-prefect-agent",
#         "networkMode": "awsvpc",
#         "revision": 2,
#         "volumes": [],
#         "status": "ACTIVE",
#         "placementConstraints": [],
#         "compatibilities": ["EC2", "FARGATE"],
#         "requiresCompatibilities": ["FARGATE"],
#         "cpu": "1024",
#         "memory": "2048",
#         "registeredAt": "2022-12-19T22:36:58.506Z",
#         "registeredBy": "arn:aws:sts::455346737763:assumed-role/AWSReservedSSO_AdministratorAccess_fe1980cf6870d6ed/george@prefect.io",
#         "tags": [],
#     }
# {
#     "logDriver": "awslogs",
#     "options": {
#         "awslogs-create-group": "true",
#         "awslogs-group": "prefect",
#         "awslogs-region": "us-east-1",
#         "awslogs-stream-prefix": "prefect",
#     },
# },
# )

basic_ecs.save("prod", overwrite=True)
s3_storage.save("se-prod", overwrite=True)
