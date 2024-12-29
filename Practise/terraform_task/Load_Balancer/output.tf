output "lbDNS" {
  value = aws_lb.task_lb.dns_name
}
output "TG" {
  value = aws_lb_target_group.task_TG.id
}
