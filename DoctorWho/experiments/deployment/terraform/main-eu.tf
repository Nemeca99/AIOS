# CARMA Mycelium Network - Europe Region
# Total Blocks: 19,047,619
# Total Capacity: 1,142,857,140 users

terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

variable "aws_region" {
  description = "AWS region for Europe"
  type        = string
  default     = "us-east-1"
}

# VPC for Europe
resource "aws_vpc" "carma_eu" {
  cidr_block           = "10.eu.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "carma-eu-vpc"
    Region = "EU"
    App = "carma-mycelium"
  }
}

# Internet Gateway
resource "aws_internet_gateway" "carma_eu_igw" {
  vpc_id = aws_vpc.carma_eu.id

  tags = {
    Name = "carma-eu-igw"
  }
}

# Subnet
resource "aws_subnet" "carma_eu_subnet" {
  vpc_id            = aws_vpc.carma_eu.id
  cidr_block        = "10.eu.1.0/24"
  availability_zone = "us-east-1a"

  tags = {
    Name = "carma-eu-subnet"
  }
}

# Security Group
resource "aws_security_group" "carma_eu_sg" {
  name_prefix = "carma-eu-"
  vpc_id      = aws_vpc.carma_eu.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
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
    Name = "carma-eu-sg"
  }
}

# Launch Template
resource "aws_launch_template" "carma_eu_template" {
  name_prefix   = "carma-eu-"
  image_id      = "ami-0c02fb55956c7d316"
  instance_type = "t3.micro"

  vpc_security_group_ids = [aws_security_group.carma_eu_sg.id]

  tag_specifications {
    resource_type = "instance"
    tags = {
      Name = "carma-eu-instance"
      Region = "EU"
      App = "carma-mycelium"
    }
  }
}

# Auto Scaling Group
resource "aws_autoscaling_group" "carma_eu_asg" {
  name                = "carma-eu-asg"
  vpc_zone_identifier = [aws_subnet.carma_eu_subnet.id]
  health_check_type   = "EC2"
  health_check_grace_period = 300

  min_size         = 1
  max_size         = 1000
  desired_capacity = 100

  launch_template {
    id      = aws_launch_template.carma_eu_template.id
    version = "$Latest"
  }

  tag {
    key                 = "Name"
    value               = "carma-eu-asg"
    propagate_at_launch = false
  }
}
