# CARMA Mycelium Network - Oceania Region
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
  description = "AWS region for Oceania"
  type        = string
  default     = "us-east-1"
}

# VPC for Oceania
resource "aws_vpc" "carma_oc" {
  cidr_block           = "10.oc.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "carma-oc-vpc"
    Region = "OC"
    App = "carma-mycelium"
  }
}

# Internet Gateway
resource "aws_internet_gateway" "carma_oc_igw" {
  vpc_id = aws_vpc.carma_oc.id

  tags = {
    Name = "carma-oc-igw"
  }
}

# Subnet
resource "aws_subnet" "carma_oc_subnet" {
  vpc_id            = aws_vpc.carma_oc.id
  cidr_block        = "10.oc.1.0/24"
  availability_zone = "us-east-1a"

  tags = {
    Name = "carma-oc-subnet"
  }
}

# Security Group
resource "aws_security_group" "carma_oc_sg" {
  name_prefix = "carma-oc-"
  vpc_id      = aws_vpc.carma_oc.id

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
    Name = "carma-oc-sg"
  }
}

# Launch Template
resource "aws_launch_template" "carma_oc_template" {
  name_prefix   = "carma-oc-"
  image_id      = "ami-0c02fb55956c7d316"
  instance_type = "t3.micro"

  vpc_security_group_ids = [aws_security_group.carma_oc_sg.id]

  tag_specifications {
    resource_type = "instance"
    tags = {
      Name = "carma-oc-instance"
      Region = "OC"
      App = "carma-mycelium"
    }
  }
}

# Auto Scaling Group
resource "aws_autoscaling_group" "carma_oc_asg" {
  name                = "carma-oc-asg"
  vpc_zone_identifier = [aws_subnet.carma_oc_subnet.id]
  health_check_type   = "EC2"
  health_check_grace_period = 300

  min_size         = 1
  max_size         = 1000
  desired_capacity = 100

  launch_template {
    id      = aws_launch_template.carma_oc_template.id
    version = "$Latest"
  }

  tag {
    key                 = "Name"
    value               = "carma-oc-asg"
    propagate_at_launch = false
  }
}
