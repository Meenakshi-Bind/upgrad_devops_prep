variable "public_subnet" {
  type = string
}
variable "eip_address" {
  type = string
}
variable "private_subnet" {
  type = string
}
variable "vpc_id" {
  type = string
}
variable "bastion_instance_id" {
  type = string
}

resource "aws_lb" "task_lb" {
  name               = "task-lb-tf"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.ALB_sg.id]
  subnet_mapping {
    subnet_id     = var.public_subnet
    allocation_id = var.eip_address
  }
  subnet_mapping {
    subnet_id     = var.private_subnet
    allocation_id = var.eip_address
  }
}


resource "aws_lb_target_group" "task_TG" {
  name        = "tf-lb-tg"
  port        = 80
  protocol    = "HTTP"
  vpc_id      = var.vpc_id
  target_type = "instance"
}

resource "aws_lb_target_group_attachment" "tG_attach" {
  target_group_arn = aws_lb_target_group.task_TG.arn
  target_id        = var.bastion_instance_id
  port             = 80
}

resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.task_lb.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.task_TG.arn
  }
}

#security group for ALB
resource "aws_security_group" "ALB_sg" {
  name        = "sg og ALB"
  description = "Security group for Public Web instances"
  vpc_id      = var.vpc_id

  # Allow HTTP traffic (port 80) from self IP
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
    Name = "SG for ALB"
  }
}