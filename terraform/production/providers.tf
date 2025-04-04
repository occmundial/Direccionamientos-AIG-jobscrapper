provider "aws" {
  region = "us-west-2"
  default_tags {
    tags = {
      Domain = var.org_id
      map-migrated = var.migration_id
    }
  }
}

terraform {
  required_version = "~> 1.4.4"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.64.0"
    }
  }
}