variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "eu-west-1"
}

variable "ami_id" {
  description = "Ubuntu AMI ID"
  type        = string
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t2.micro"
}

variable "sg_name" {
  description = "Security group name"
  type        = string
  default     = "terraform-web-sg"
}

variable "instance_name" {
  description = "EC2 instance name"
  type        = string
  default     = "terraform-web-server"
}