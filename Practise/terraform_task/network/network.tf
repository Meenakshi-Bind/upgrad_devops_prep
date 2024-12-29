variable "cidr_block_VPC" {
  type = string
}
variable "cidr_block_private_1" {
  type = string
}
variable "cidr_block_private_2" {
  type = string
}
variable "cidr_block_public_1" {
  type = string
}
variable "cidr_block_public_2" {
  type = string
}
variable "AZ_1" {
  type = string
}
variable "AZ_2" {
  type = string
}


##VPC
resource "aws_vpc" "vpc" {
  cidr_block = var.cidr_block_VPC
}
##subnets
resource "aws_subnet" "public1" {
  vpc_id     = aws_vpc.vpc.id
  cidr_block = var.cidr_block_public_1

  availability_zone = var.AZ_1

}
resource "aws_subnet" "public2" {
  vpc_id            = aws_vpc.vpc.id
  cidr_block        = var.cidr_block_public_2
  availability_zone = var.AZ_2

}
resource "aws_subnet" "private1" {
  vpc_id            = aws_vpc.vpc.id
  cidr_block        = var.cidr_block_private_1
  availability_zone = var.AZ_1

}
resource "aws_subnet" "private2" {
  vpc_id            = aws_vpc.vpc.id
  cidr_block        = var.cidr_block_private_2
  availability_zone = var.AZ_2

}

##IGW
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.vpc.id

}

##NAT
resource "aws_nat_gateway" "taskNAT" {
  allocation_id = aws_eip.natEip.id
  subnet_id     = aws_subnet.public1.id
  depends_on    = [aws_internet_gateway.igw]
}

##EIP
resource "aws_eip" "natEip" {
  domain = "vpc"
}

##route table public

resource "aws_route_table" "rtPublic" {
  vpc_id = aws_vpc.vpc.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }



}

##subnets association public RT
resource "aws_route_table_association" "pub1" {
  subnet_id      = aws_subnet.public1.id
  route_table_id = aws_route_table.rtPublic.id
}
resource "aws_route_table_association" "pub2" {
  subnet_id      = aws_subnet.public2.id
  route_table_id = aws_route_table.rtPublic.id
}


##route table private

resource "aws_route_table" "rtPrivate" {
  vpc_id = aws_vpc.vpc.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.taskNAT.id
  }


}
##subnets association private RT
resource "aws_route_table_association" "pri1" {
  subnet_id      = aws_subnet.private1.id
  route_table_id = aws_route_table.rtPrivate.id
}
resource "aws_route_table_association" "pri2" {
  subnet_id      = aws_subnet.private2.id
  route_table_id = aws_route_table.rtPrivate.id
}


