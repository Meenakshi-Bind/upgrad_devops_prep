output "bashian_instance" {
  value = aws_instance.bastian_Ec2.id
}

output "jenkins_instance" {
  value = aws_instance.jenkins_Ec2.id
}

output "app_instance" {
  value = aws_instance.app_Ec2.id
}

output "private_key_pem" {
  value     = tls_private_key.prikey.private_key_openssh
}
