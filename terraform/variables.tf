variable "region" {
  default = "ap-south-1"
}

variable "instance_type" {
  default = "t2.micro"
}

variable "aws_access_key" {
  description = "AWS access key"
}

variable "aws_secret_key" {
  description = "AWS secret key"
  sensitive   = true
}

variable "key_name" {
  description = "AWS key pair name for SSH"
}

# DockerHub credentials
variable "dockerhub_username" {
  description = "DockerHub username"
}

variable "dockerhub_token" {
  description = "DockerHub token"
  sensitive   = true
}
