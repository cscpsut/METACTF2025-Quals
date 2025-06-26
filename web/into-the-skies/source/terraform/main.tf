provider "aws" {
  region = var.region
}

data "aws_caller_identity" "current" {}
data "aws_availability_zones" "azs"   { state = "available" }

# ---------------------------------------------------------------------------
# 1) NETWORK – VPC, subnets, IGW, NAT, route tables
# ---------------------------------------------------------------------------
locals {
  vpc_cidr             = "10.0.0.0/16"
  public_subnet_cidrs  = ["10.0.1.0/24", "10.0.2.0/24"]
  private_subnet_cidrs = ["10.0.11.0/24", "10.0.12.0/24"]
}

resource "aws_vpc" "main" {
  cidr_block           = local.vpc_cidr
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags = { Name = "main-vpc" }
}

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.main.id
  tags   = { Name = "main-igw" }
}

# ---- Subnets --------------------------------------------------------------
resource "aws_subnet" "public" {
  for_each                = toset(local.public_subnet_cidrs)
  vpc_id                  = aws_vpc.main.id
  cidr_block              = each.key
  availability_zone       = element(data.aws_availability_zones.azs.names, index(local.public_subnet_cidrs, each.key))
  map_public_ip_on_launch = true
  tags = { Name = "public-${each.key}" }
}

resource "aws_subnet" "private" {
  for_each          = toset(local.private_subnet_cidrs)
  vpc_id            = aws_vpc.main.id
  cidr_block        = each.key
  availability_zone = element(data.aws_availability_zones.azs.names, index(local.private_subnet_cidrs, each.key))
  tags = { Name = "private-${each.key}" }
}

# ---- Routing --------------------------------------------------------------
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }
  tags = { Name = "public-rt" }
}
resource "aws_route_table_association" "public_assoc" {
  for_each       = aws_subnet.public
  subnet_id      = each.value.id
  route_table_id = aws_route_table.public.id
}


resource "aws_eip" "nat_eip" { domain = "vpc" }
resource "aws_nat_gateway" "nat" {
  allocation_id = aws_eip.nat_eip.id
  subnet_id     = element(values(aws_subnet.public)[*].id, 0)   
  tags          = { Name = "main-nat" }
}

resource "aws_route_table" "private" {
  vpc_id = aws_vpc.main.id
  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.nat.id
  }
  tags   = { Name = "private-rt" }
}
resource "aws_route_table_association" "private_assoc" {
  for_each       = aws_subnet.private
  subnet_id      = each.value.id
  route_table_id = aws_route_table.private.id
}

# ---------------------------------------------------------------------------
# 2) SECURITY GROUPS
# ---------------------------------------------------------------------------
resource "aws_security_group" "alb_sg" {
  name        = "alb-sg"
  description = "ALB allows HTTP from within VPC"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = [local.vpc_cidr]   
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "ec2_sg" {
  name   = "ec2-sg"
  vpc_id = aws_vpc.main.id

  ingress {
    from_port       = 80
    to_port         = 80
    protocol        = "tcp"
    security_groups = [aws_security_group.alb_sg.id]   # only ALB
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}


resource "aws_iam_role" "ec2_role" {
  name = "ec2-secrets-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect    = "Allow",
      Principal = { Service = "ec2.amazonaws.com" },
      Action    = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_policy" "secrets_access" {
  name   = "SecretsManagerFlagAccess"
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect   = "Allow",
        Action   = ["secretsmanager:GetSecretValue"],
        Resource = "arn:aws:secretsmanager:us-east-1:478277449877:secret:flag-ZMG5dL"
      },
      {
        Effect   = "Allow",
        Action   = ["secretsmanager:ListSecrets"],
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "role_attach" {
  role       = aws_iam_role.ec2_role.name
  policy_arn = aws_iam_policy.secrets_access.arn
}

resource "aws_iam_instance_profile" "ec2_profile" {
  name = "ec2-instance-profile"
  role = aws_iam_role.ec2_role.name
}

# ---------------------------------------------------------------------------
# 4) LAUNCH TEMPLATE
# ---------------------------------------------------------------------------
data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]
  filter {
    name   = "name"
    values = [var.ami_name_filter]
  }
}

resource "aws_launch_template" "web_lt" {
  name_prefix   = "web-lt-"
  image_id      = "ami-03a3dd5a8ecd5e0c5"
  instance_type = var.instance_type
  # key_name      = var.key_name

  iam_instance_profile { name = aws_iam_instance_profile.ec2_profile.name }
  vpc_security_group_ids = [aws_security_group.ec2_sg.id]

  metadata_options {
    http_endpoint               = "enabled"
    http_tokens                 = "optional"  
    http_put_response_hop_limit = 2
  }

user_data = base64encode(<<EOF
#!/bin/bash


systemctl daemon-reexec
systemctl daemon-reload
systemctl enable flaskapp.service
systemctl start flaskapp.service

echo "OK" > /var/www/html/health.html
chown www-data:www-data /var/www/html/health.html
EOF
)
}

# ---------------------------------------------------------------------------
# 5) PRIVATE ALB + TG + LISTENER
# ---------------------------------------------------------------------------
resource "aws_lb" "app_alb" {
  name               = "app-alb"
  internal           = true                   
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb_sg.id]
  subnets            = [for s in aws_subnet.private : s.id]
}

resource "aws_lb_target_group" "app_tg" {
  name        = "app-tg"
  port        = 80
  protocol    = "HTTP"
  vpc_id      = aws_vpc.main.id
  target_type = "instance"
  health_check { path = "/" }
}

resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.app_alb.arn
  port              = 80
  protocol          = "HTTP"
  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.app_tg.arn
  }
}

# ---------------------------------------------------------------------------
# 6) AUTO SCALING GROUP
# ---------------------------------------------------------------------------
resource "aws_autoscaling_group" "web_asg" {
  name               = "web-asg"
  min_size           = 1
  desired_capacity   = var.desired_capacity
  max_size           = 4
  default_cooldown       = 300
  vpc_zone_identifier = [for s in aws_subnet.private : s.id]

  launch_template {
    id      = aws_launch_template.web_lt.id
    version = "$Latest"
  }

  target_group_arns = [aws_lb_target_group.app_tg.arn]

  tag {
    key                 = "Name"
    value               = "web-asg-instance"
    propagate_at_launch = true
  }
}

resource "aws_autoscaling_policy" "tt_requests" {
  name                   = "tt-alb-reqs"
  policy_type            = "TargetTrackingScaling"
  autoscaling_group_name = aws_autoscaling_group.web_asg.name

  target_tracking_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ALBRequestCountPerTarget"

      resource_label = "${aws_lb.app_alb.arn_suffix}/${aws_lb_target_group.app_tg.arn_suffix}"
    }

    target_value      = 100
    disable_scale_in  = false
  }
}

# ---------------------------------------------------------------------------
# 7) API GATEWAY HTTP API + VPC LINK
# ---------------------------------------------------------------------------
resource "aws_apigatewayv2_api" "http_api" {
  name          = "http-api-to-alb"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_vpc_link" "alb_link" {
  name               = "vpc-link-to-alb"
  subnet_ids         = [for s in aws_subnet.private : s.id]   # ENIs land in these subnets
  security_group_ids = [aws_security_group.alb_sg.id]
}

resource "aws_apigatewayv2_integration" "alb_integration" {
  api_id                  = aws_apigatewayv2_api.http_api.id
  integration_type        = "HTTP_PROXY"
  integration_method      = "ANY"
  connection_type         = "VPC_LINK"
  connection_id           = aws_apigatewayv2_vpc_link.alb_link.id
  integration_uri         = aws_lb_listener.http.arn
  payload_format_version  = "1.0"
}

resource "aws_apigatewayv2_route" "proxy_route" {
  api_id    = aws_apigatewayv2_api.http_api.id
  route_key = "ANY /{proxy+}"
  target    = "integrations/${aws_apigatewayv2_integration.alb_integration.id}"
}

resource "aws_apigatewayv2_stage" "default" {
  api_id      = aws_apigatewayv2_api.http_api.id
  name        = "$default"
  auto_deploy = true
}

# ---------------------------------------------------------------------------
# 8) OUTPUTS
# ---------------------------------------------------------------------------
output "api_gateway_url" {
  description = "Public entry point"
  value       = aws_apigatewayv2_api.http_api.api_endpoint
}

output "alb_dns_name" {
  description = "Private ALB DNS (only resolvable/usable inside the VPC)"
  value       = aws_lb.app_alb.dns_name
}

output "private_subnets" {
  value = [for s in aws_subnet.private : s.id]
}

output "vpc_id" {
  value = aws_vpc.main.id
}