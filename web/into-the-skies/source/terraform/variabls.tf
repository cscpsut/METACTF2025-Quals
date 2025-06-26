variable "region"          { default = "us-east-1" }
variable "key_name" {
  description = "Existing EC2 key pair"
  default     = "ansible2.pem"
}
variable "instance_type"   { default = "t3.small" }
variable "desired_capacity"{ default = 2 }
variable "ami_name_filter" { default = "amzn2-ami-hvm-*-x86_64-gp2" }
variable "secret_name"     { default = "flag" }
