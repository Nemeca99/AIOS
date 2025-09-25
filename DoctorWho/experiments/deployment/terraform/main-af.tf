# CARMA Mycelium Network - Africa Region
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
  description = "AWS region for Africa"
  type        = string
  default     = "us-east-1"
}

# VPC for Africa
resource "aws_vpc" "carma_af" {
  cidr_block           = "10.af.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "carma-af-vpc"
    Region = "AF"
    App = "carma-mycelium"
  }
}

# Internet Gateway
resource "aws_internet_gateway" "carma_af_igw" {
  vpc_id = aws_vpc.carma_af.id

  tags = {
    Name = "carma-af-igw"
  }
}

# Subnet
resource "aws_subnet" "carma_af_subnet" {
  vpc_id            = aws_vpc.carma_af.id
  cidr_block        = "10.af.1.0/24"
  availability_zone = "us-east-1a"

  tags = {
    Name = "carma-af-subnet"
  }
}

# Security Group
resource "aws_security_group" "carma_af_sg" {
  name_prefix = "carma-af-"
  vpc_id      = aws_vpc.carma_af.id

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
    Name = "carma-af-sg"
  }
}

# Launch Template
resource "aws_launch_template" "carma_af_template" {
  name_prefix   = "carma-af-"
  image_id      = "ami-0c02fb55956c7d316"
  instance_type = "t3.micro"

  vpc_security_group_ids = [aws_security_group.carma_af_sg.id]

  tag_specifications {
    resource_type = "instance"
    tags = {
      Name = "carma-af-instance"
      Region = "AF"
      App = "carma-mycelium"
    }
  }
}

# Auto Scaling Group
resource "aws_autoscaling_group" "carma_af_asg" {
  name                = "carma-af-asg"
  vpc_zone_identifier = [aws_subnet.carma_af_subnet.id]
  health_check_type   = "EC2"
  health_check_grace_period = 300

  min_size         = 1
  max_size         = 1000
  desired_capacity = 100

  launch_template {
    id      = aws_launch_template.carma_af_template.id
    version = "$Latest"
  }

  tag {
    key                 = "Name"
    value               = "carma-af-asg"
    propagate_at_launch = false
  }
}
