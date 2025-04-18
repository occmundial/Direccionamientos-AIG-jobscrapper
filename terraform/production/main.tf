locals {
  project_name = var.project_name
  secret_arn   = "arn:aws:secretsmanager:us-west-2:671249220468:secret:marketplaceservices/Direccionamientos-AIG-jobscrapper/prod/connectionstrings-qrLTDs"
  secrets = [
    {
      name      = "AAIS_SERVER"
      valueFrom = "${local.secret_arn}:AAIS_SERVER::"
    },
    {
      name      = "AAIS_TOKEN"
      valueFrom = "${local.secret_arn}:AAIS_TOKEN::"
    },
    {
      name      = "CHANNEL"
      valueFrom = "${local.secret_arn}:CHANNEL::"
    },
    {
      name      = "CHRONOS"
      valueFrom = "${local.secret_arn}:CHRONOS::"
    }
    ,
    {
      name      = "DB_HOST"
      valueFrom = "${local.secret_arn}:DB_HOST::"
    }
    ,
    {
      name      = "DB_NAME"
      valueFrom = "${local.secret_arn}:DB_NAME::"
    }
    ,
    {
      name      = "DB_PASSWORD"
      valueFrom = "${local.secret_arn}:DB_PASSWORD::"
    }
    ,
    {
      name      = "DB_USER"
      valueFrom = "${local.secret_arn}:DB_USER::"
    }
    ,
    {
      name      = "ENVIROMENT"
      valueFrom = "${local.secret_arn}:ENVIROMENT::"
    }
    ,
    {
      name      = "PASS_JOB_SCRAPPER"
      valueFrom = "${local.secret_arn}:PASS_JOB_SCRAPPER::"
    }
    ,
    {
      name      = "S3_BUCKET"
      valueFrom = "${local.secret_arn}:S3_BUCKET::"
    }
    ,
    {
      name      = "SEMANTIC"
      valueFrom = "${local.secret_arn}:SEMANTIC::"
    }
    ,
    {
      name      = "SLACK_TOKEN"
      valueFrom = "${local.secret_arn}:SLACK_TOKEN::"
    }
    ,
    {
      name      = "TLALOC"
      valueFrom = "${local.secret_arn}:TLALOC::"
    }
    ,
    {
      name      = "TLALOC_TOKEN"
      valueFrom = "${local.secret_arn}:TLALOC_TOKEN::"
    }
    ,
    {
      name      = "TOKEN_SEMANTIC"
      valueFrom = "${local.secret_arn}:TOKEN_SEMANTIC::"
    }
    ,
    {
      name      = "USR_JOB_SCRAPPER"
      valueFrom = "${local.secret_arn}:USR_JOB_SCRAPPER::"
    }
    ,
    {
      name      = "WSDL_AUTH_CLIENT"
      valueFrom = "${local.secret_arn}:WSDL_AUTH_CLIENT::"
    }
    ,
    {
      name      = "WSDL_CLIENT"
      valueFrom = "${local.secret_arn}:WSDL_CLIENT::"
    }
    ,
    {
      name      = "S3_KEY"
      valueFrom = "${local.secret_arn}:S3_KEY::"
    }
  ]
  
}

module "batch-job" {
  source           = "git::git@github.com:occmundial/tf-modules.git//occ-batch-job"
  vpc_id           = "vpc-0701753a47d98ea5d"
  project_name     = local.project_name
  subnets          = ["subnet-016a4d39c397e00e6", "subnet-09aef403b11db453a", "subnet-01430b637c4da2272"]
  max_vcpus        = 8
  container_memory = 8192
  container_cpus   = 4
  logdriver        = "awslogs"
  repo             = var.repo_name
  image            = var.image
  command          = ["python","-i","main.py"]
  secrets          = local.secrets
  secret_arn       = local.secret_arn
  kms_arn          = "arn:aws:kms:us-west-2:671249220468:key/8bfa5283-10be-4cf4-b321-811e159a3538"
}

module "occ-eventbridge" {
  source              = "git::git@github.com:occmundial/tf-modules.git//occ-eventbridge"
  schedule_expression = "cron(0 */2 ? * * *)"
  project_name        = local.project_name
  job_queue_arn       = module.batch-job.job_queue_arn
  job_definition      = module.batch-job.job_definition
  job_name            = local.project_name
  depends_on = [
    module.batch-job
  ]
}

resource "aws_iam_policy" "s3_access" {
  name        = "${var.project_name}-bucket-access-policy-occ-direcc"  
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect   = "Allow"
        Action   = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:ListBucket"
        ]
        Resource = [
          "arn:aws:s3:::occ-direcc",
          "arn:aws:s3:::occ-direcc/*"
        ]
      }
    ]
  })
}


resource "aws_iam_role_policy_attachment" "attach_s3_policy" {
  policy_arn = aws_iam_policy.s3_access.arn
  role       = "${var.project_name}-exec-role"
}

