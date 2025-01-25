variable "ami" {
  type = string
}
variable "instanceType" {
  type = string
}
variable "pubsubnetId" {
  type = string
}
variable "pri1subnetId" {
  type = string
}
variable "pri2subnetId" {
  type = string
}
# Variables
variable "vpc_id" {
  description = "The ID of the VPC"
  type        = string
}

variable "cidr_block" {
  description = "CIDR block of the VPC"
  type        = string
}

variable "selfip" {
  description = "CIDR block of the VPC"
  type        = string
}
variable "instance_profile_name" {
  type = string
}

# Bastion Host Security Group
resource "aws_security_group" "bastion_sg" {
  name        = "bastion-sg"
  description = "Security group for Bastion Host"
  vpc_id      = var.vpc_id

  # Allow SSH access from self IP
  ingress {
    description = "Allow SSH from self IP"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow all outbound traffic
  egress {
    description = "Allow all egress"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    description = "Allow HTTP traffic from self IP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow all outbound traffic
  egress {
    description = "Allow all egress"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  tags = {
    Name = "Bastion Host SG"
  }
}

# Private Instances Security Group
resource "aws_security_group" "private_instances_sg" {
  name        = "private-instances-sg"
  description = "Security group for Private Instances"
  vpc_id      = var.vpc_id

  # Allow all traffic from within the VPC
  ingress {
    description = "Allow all traffic from VPC"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = [var.cidr_block]
  }

  # Allow all outbound traffic
  egress {
    description = "Allow all egress"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
# Allow SSH access from self IP
  ingress {
    description = "Allow SSH from self IP"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow all outbound traffic
  egress {
    description = "Allow all egress"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    description = "Allow HTTP traffic from self IP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow all outbound traffic
  egress {
    description = "Allow all egress"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  tags = {
    Name = "Private Instances SG"
  }
}

# Public Web Security Group
resource "aws_security_group" "public_web_sg" {
  name        = "public-web-sg"
  description = "Security group for Public Web instances"
  vpc_id      = var.vpc_id

  # Allow HTTP traffic (port 80) from self IP
  ingress {
    description = "Allow HTTP traffic from self IP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = [format("%s/32", var.selfip)] 
  }

  # Allow all outbound traffic
  egress {
    description = "Allow all egress"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
# Allow SSH access from self IP
  ingress {
    description = "Allow SSH from self IP"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow all outbound traffic
  egress {
    description = "Allow all egress"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    description = "Allow HTTP traffic from self IP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow all outbound traffic
  egress {
    description = "Allow all egress"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  tags = {
    Name = "Public Web SG"
  }
}

resource "aws_instance" "bastian_Ec2" {
  ami                         = var.ami
  instance_type               = var.instanceType
  subnet_id                   = var.pubsubnetId
  key_name                    = aws_key_pair.keypair.key_name
  iam_instance_profile = var.instance_profile_name
  associate_public_ip_address = true
  vpc_security_group_ids = [
    aws_security_group.bastion_sg.id
  ]
  tags = {
    Name = "bashian_instance"
  }
}

resource "aws_instance" "jenkins_Ec2" {
  ami           = var.ami
  instance_type = var.instanceType
  subnet_id     = var.pri1subnetId
  key_name      = aws_key_pair.keypair.key_name
  iam_instance_profile = var.instance_profile_name
  vpc_security_group_ids = [
    aws_security_group.private_instances_sg.id
  ]
  tags = {
    Name = "jenkins_instance"
  }
}

resource "aws_instance" "app_Ec2" {
  ami           = var.ami
  instance_type = var.instanceType
  subnet_id     = var.pri2subnetId
  key_name      = aws_key_pair.keypair.key_name
  iam_instance_profile = var.instance_profile_name
  vpc_security_group_ids = [
    aws_security_group.public_web_sg.id
  ]
  tags = {
    Name = "app_instance"
  }
}

resource "tls_private_key" "prikey" {
  algorithm = "RSA"
  rsa_bits  = 2048
}

resource "aws_key_pair" "keypair" {
  key_name   = "my-generated-key"
  public_key = tls_private_key.prikey.public_key_openssh
}


resource "local_sensitive_file" "this" {
  content  = tls_private_key.prikey.private_key_openssh
  filename = "sshkey-${aws_key_pair.keypair.key_name}"
}
