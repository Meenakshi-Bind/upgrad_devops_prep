terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.76.0"
    }
  }
  backend "s3" {
    bucket = "terraform-store-tf"
    key    = "terraformfile/terraform.tfstate"
    region = "us-east-1"
  }
}

provider "aws" {
  # Configuration options
  region = "us-east-1"
}


# Simple S3 bucket creation
resource "aws_s3_bucket" "terraform_state" {
  bucket = "terraform-store-tf-try"
}