terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.76.0"
    }
  }
  backend "s3" {
    bucket = "terraform-research-in-computing"
    key    = "terraformfile/terraform.tfstate"
    region = "us-east-1"
  }
}

provider "aws" {
  region = var.aws_region
}

# Start timer
resource "null_resource" "start_timer" {
  provisioner "local-exec" {
    command = <<EOT
START=$(date '+%Y-%m-%d %H:%M:%S')
START_EPOCH=$(date +%s)

echo $START > start_time.txt
echo $START_EPOCH > start_epoch.txt

echo "------------------------------------"
echo "Terraform deployment started at: $START"
echo "------------------------------------"
EOT
  }
}

resource "aws_security_group" "web_sg" {
  depends_on = [null_resource.start_timer]

  name        = var.sg_name
  description = "Allow SSH and HTTP"

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = var.sg_name
  }
}

resource "aws_instance" "web_server" {
  depends_on = [aws_security_group.web_sg]

  ami                    = var.ami_id
  instance_type          = var.instance_type
  vpc_security_group_ids = [aws_security_group.web_sg.id]

  user_data = <<-EOF
              #!/bin/bash
              apt update -y
              apt install apache2 -y
              systemctl start apache2
              systemctl enable apache2
              echo "<h1>Terraform Deployment Success</h1>" > /var/www/html/index.html
              EOF

  tags = {
    Name = var.instance_name
  }
}

# End timer
resource "null_resource" "end_timer" {
  depends_on = [aws_instance.web_server]

  provisioner "local-exec" {
    command = <<EOT
END=$(date '+%Y-%m-%d %H:%M:%S')
END_EPOCH=$(date +%s)

START=$(cat start_time.txt)
START_EPOCH=$(cat start_epoch.txt)

TOTAL=$((END_EPOCH - START_EPOCH))

echo "------------------------------------"
echo "Start Time : $START"
echo "End Time   : $END"
echo "Total Time : $TOTAL seconds"
echo "------------------------------------"
EOT
  }
}