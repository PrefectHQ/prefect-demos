from prefect_aws import ECSTask

ib_1_17 = ECSTask(
    image="455346737763.dkr.ecr.us-east-2.amazonaws.com/prefect-se-dev:2-latest",
    vpc_id="vpc-0176a93c6464344f9",
    cluster="prefect-agent-taylor_test_1_17",
    execution_role_arn="arn:aws:iam::455346737763:role/prefect-agent-execution-role-se-dev-ecs-on-fargate",
    task_customizations=[
        {
            "op": "add",
            "path": "/networkConfiguration/awsvpcConfiguration/securityGroups",
            "value": [
                "sg-05f6068ed4bc44860"
            ]
        }
    ],
    task_start_timeout_seconds=600
)

ib_1_17.save("tay-ib-1-17", overwrite=True)