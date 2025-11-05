# ----------------------------
# Fetch latest Ubuntu 20.04 LTS x86_64 AMI
# ----------------------------
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"]  # Canonical AWS account ID

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }
}

# ----------------------------
# Security Group for EC2
# ----------------------------
resource "aws_security_group" "app_sg" {
  name        = "app-sg"
  description = "Allow SSH, HTTP, and FastAPI port"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # SSH
  }

  ingress {
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # FastAPI
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# ----------------------------
# EC2 Instance
# ----------------------------
resource "aws_instance" "fastapi_ec2" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = var.instance_type
  key_name      = var.key_name

  user_data = <<-EOF
              #!/bin/bash
              apt update -y
              apt install docker.io -y
              systemctl start docker
              systemctl enable docker
              docker login -u ${var.dockerhub_username} -p ${var.dockerhub_token}
              docker run -d -p 8000:8000 ${var.dockerhub_username}/mlops-capstone:latest
              EOF

  security_groups = [aws_security_group.app_sg.name]

  tags = {
    Name = "fastapi-server"
  }
}

# ----------------------------
# Output public IP
# ----------------------------
output "public_ip" {
  value = aws_instance.fastapi_ec2.public_ip
}
