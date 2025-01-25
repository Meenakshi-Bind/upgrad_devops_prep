variable "cidr_block_VPC" {
  type    = string
  default = "10.100.0.0/16"
}

variable "cidr_block_public_1" {
  type    = string
  default = "10.100.1.0/24"
}

variable "cidr_block_public_2" {
  type    = string
  default = "10.100.2.0/24"
}

variable "cidr_block_private_1" {
  type    = string
  default = "10.100.3.0/24"
}

variable "cidr_block_private_2" {
  type    = string
  default = "10.100.4.0/24"
}

variable "AZ_1" {
  type    = string
  default = "us-east-1a"
}

variable "AZ_2" {
  type    = string
  default = "us-east-1b"
}

variable "ami" {
  type    = string
  default = "ami-0866a3c8686eaeeba"
}

variable "ec2Type" {
  type    = string
  default = "t2.micro"
}
variable "iam_role_name" {
  type    = string
  default = "task_role"
}