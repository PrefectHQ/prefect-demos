provider "aws" {
  region = "us-east-2"
}
module "prefect_ecs_agent" {
  # source = "github.com/PrefectHQ/prefect-recipes//devops/infrastructure-as-code/aws/tf-prefect2-ecs-agent"
  source = "git::https://github.com/PrefectHQ/prefect-recipes//devops/infrastructure-as-code/aws/tf-prefect2-ecs-agent?ref=tf-ecs-task-role"

  vpc_id               = var.vpc_id
  agent_subnets        = var.agent_subnets
  agent_queue_name     = "ecs-agent-test-1-17"
  name                 = "taylor_test_1_17"
  prefect_account_id   = var.prefect_account_id
  prefect_api_key      = var.prefect_api_key
  prefect_workspace_id = var.prefect_workspace_id
  agent_image          = "455346737763.dkr.ecr.us-east-2.amazonaws.com/prefect-aws:latest"
}