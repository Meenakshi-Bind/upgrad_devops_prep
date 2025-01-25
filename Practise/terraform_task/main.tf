terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.77.0"
    }
  }
  backend "s3" {
    bucket = "terraform-tfstate-file-storage-for-project"
    key    = "tfStateStore/terraform.tfstate"
    region = "us-east-1"
  }
}

provider "aws" {
  # Configuration options
  region = "us-east-1"
}

data "http" "self_ip" {
  url = "http://ipv4.icanhazip.com"
}
module "IAM" {
  source = "./IAM"
  iam    = var.iam_role_name
}

module "network" {
  source               = "./network"
  cidr_block_VPC       = var.cidr_block_VPC
  cidr_block_private_1 = var.cidr_block_private_1
  cidr_block_private_2 = var.cidr_block_private_2
  cidr_block_public_1  = var.cidr_block_public_1
  cidr_block_public_2  = var.cidr_block_public_2
  AZ_1                 = var.AZ_1
  AZ_2                 = var.AZ_2

}
module "instance" {
  source                = "./instance"
  ami                   = var.ami
  instanceType          = var.ec2Type
  pubsubnetId           = module.network.pub1
  pri1subnetId          = module.network.pri1
  pri2subnetId          = module.network.pri2
  cidr_block            = var.cidr_block_VPC
  vpc_id                = module.network.vpc
  selfip                = trimspace(data.http.self_ip.body)
  instance_profile_name = module.IAM.task_instance_profile_name
}
module "Load_Balancer" {
  source              = "./Load_Balancer"
  public_subnet       = module.network.pub1
  eip_address         = module.network.nateip
  private_subnet      = module.network.pri2
  vpc_id              = module.network.vpc
  bastion_instance_id = module.instance.bashian_instance

}

