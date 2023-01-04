provider "aws" {
  region = "us-east-2"
}
module "prefect_ecs_agent" {
  # source = "github.com/PrefectHQ/prefect-recipes//devops/infrastructure-as-code/aws/tf-prefect2-ecs-agent"
  source = "git::https://github.com/PrefectHQ/prefect-recipes//devops/infrastructure-as-code/aws/tf-prefect2-ecs-agent?ref=ecs-service-change"

  vpc_id               = "vpc-0176a93c6464344f9"
  agent_subnets        = ["subnet-01a7a00f7cf3db089"]
  agent_queue_name     = "ecs-agent-0"
  name                 = "taylor_agent_0"
  prefect_account_id   = var.prefect_account_id
  prefect_api_key      = var.prefect_api_key
  prefect_workspace_id = var.prefect_workspace_id
  agent_image          = "455346737763.dkr.ecr.us-east-2.amazonaws.com/prefect-aws:latest"
}