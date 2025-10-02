terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "6.14.0"
    }
  }
}

terraform {
  backend "s3" {
    bucket = "tfstatefilestoragetest"
    key    = "tfstatefile/terraform.tfstate"
    region = "us-east-1"
  }
}

provider "aws" {
    region = "us-east-1"
}