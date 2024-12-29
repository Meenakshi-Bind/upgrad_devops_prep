output "vpc" {
  value = aws_vpc.vpc.id
}

output "pub1" {
  value = aws_subnet.public1.id
}

output "pub2" {
  value = aws_subnet.public2.id
}

output "pri1" {
  value = aws_subnet.private1.id
}

output "pri2" {
  value = aws_subnet.private2.id
}

output "igw" {
  value = aws_internet_gateway.igw.id
}
output "nat" {
  value = aws_nat_gateway.taskNAT.id
}

output "nateip" {
  value = aws_eip.natEip.address
}
output "rtPub" {
  value = aws_route_table.rtPublic.id
}

output "rtPri" {
  value = aws_route_table.rtPrivate.id
}

