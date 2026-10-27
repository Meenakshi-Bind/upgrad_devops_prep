#!/bin/bash

# Exit on error
set -e

# Variables
REGION="us-east-1"
DJANGO_SECRET_KEY="$1"  # Removed DB_PASSWORD parameter
EB_SG_NAME="parking-app-eb-sg"
EB_APP_NAME="parking-app"
EB_ENV_NAME="parking-app-env"

echo "Starting infrastructure deployment..."

# Function to check if resource exists
check_resource_exists() {
    local resource_type="$1"
    local resource_name="$2"
    
    case $resource_type in
        "security-group")
            aws ec2 describe-security-groups --group-names "$resource_name" --region $REGION >/dev/null 2>&1
            ;;
        "elasticbeanstalk-app")
            aws elasticbeanstalk describe-applications --application-name "$resource_name" --region $REGION >/dev/null 2>&1
            ;;
        "elasticbeanstalk-env")
            aws elasticbeanstalk describe-environments --application-name "$EB_APP_NAME" --environment-names "$resource_name" --region $REGION >/dev/null 2>&1
            ;;
    esac
    return $?
}

# 1. Create Security Group for Elastic Beanstalk
echo "Step 1: Creating Elastic Beanstalk Security Group..."
if ! check_resource_exists "security-group" "$EB_SG_NAME"; then
    EB_SG_ID=$(aws ec2 create-security-group \
        --group-name "$EB_SG_NAME" \
        --description "Security group for Elastic Beanstalk" \
        --region $REGION \
        --query 'GroupId' \
        --output text)
    
    # Add ingress rules
    aws ec2 authorize-security-group-ingress \
        --group-id "$EB_SG_ID" \
        --protocol tcp \
        --port 80 \
        --cidr 0.0.0.0/0 \
        --region $REGION
    
    aws ec2 authorize-security-group-ingress \
        --group-id "$EB_SG_ID" \
        --protocol tcp \
        --port 443 \
        --cidr 0.0.0.0/0 \
        --region $REGION
    
    echo "EB Security Group created: $EB_SG_ID"
else
    EB_SG_ID=$(aws ec2 describe-security-groups \
        --group-names "$EB_SG_NAME" \
        --region $REGION \
        --query 'SecurityGroups[0].GroupId' \
        --output text)
    echo "EB Security Group already exists: $EB_SG_ID"
fi

# 2. Create Elastic Beanstalk Application
echo "Step 2: Creating Elastic Beanstalk Application..."
if ! check_resource_exists "elasticbeanstalk-app" "$EB_APP_NAME"; then
    aws elasticbeanstalk create-application \
        --application-name "$EB_APP_NAME" \
        --description "Car Parking Management Application" \
        --region $REGION
    echo "Elastic Beanstalk Application created"
else
    echo "Elastic Beanstalk Application already exists"
fi

# 3. Create Elastic Beanstalk Environment
echo "Step 3: Creating Elastic Beanstalk Environment..."
if ! check_resource_exists "elasticbeanstalk-env" "$EB_ENV_NAME"; then
    # Create option settings file (removed DATABASE_URL)
    cat > /tmp/eb-options.json << EOF
[
    {
        "Namespace": "aws:autoscaling:launchconfiguration",
        "OptionName": "IamInstanceProfile",
        "Value": "LabInstanceProfile"
    },
    {
        "Namespace": "aws:autoscaling:launchconfiguration",
        "OptionName": "EC2KeyName",
        "Value": "vockey"
    },
    {
        "Namespace": "aws:autoscaling:launchconfiguration",
        "OptionName": "InstanceType",
        "Value": "t2.micro"
    },
    {
        "Namespace": "aws:elasticbeanstalk:environment",
        "OptionName": "ServiceRole",
        "Value": "LabRole"
    },
    {
        "Namespace": "aws:elasticbeanstalk:environment",
        "OptionName": "EnvironmentType",
        "Value": "LoadBalanced"
    },
    {
        "Namespace": "aws:elasticbeanstalk:environment",
        "OptionName": "LoadBalancerType",
        "Value": "application"
    },
    {
        "Namespace": "aws:autoscaling:asg",
        "OptionName": "MinSize",
        "Value": "1"
    },
    {
        "Namespace": "aws:autoscaling:asg",
        "OptionName": "MaxSize",
        "Value": "2"
    },
    {
        "Namespace": "aws:elasticbeanstalk:application:environment",
        "OptionName": "DJANGO_SETTINGS_MODULE",
        "Value": "parking_project.settings.production"
    },
    {
        "Namespace": "aws:elasticbeanstalk:application:environment",
        "OptionName": "SECRET_KEY",
        "Value": "$DJANGO_SECRET_KEY"
    },
    {
        "Namespace": "aws:elasticbeanstalk:application:environment",
        "OptionName": "DEBUG",
        "Value": "False"
    },
    {
        "Namespace": "aws:elasticbeanstalk:application:environment",
        "OptionName": "ALLOWED_HOSTS",
        "Value": "*"
    }
]
EOF
    
    aws elasticbeanstalk create-environment \
        --application-name "$EB_APP_NAME" \
        --environment-name "$EB_ENV_NAME" \
        --solution-stack-name "64bit Amazon Linux 2023 v4.0.1 running Python 3.11" \
        --option-settings file:///tmp/eb-options.json \
        --region $REGION \
        --tags "Key=Project,Value=ParkingApp"
    
    echo "Elastic Beanstalk Environment creation initiated"
    
    # Wait for environment to be ready
    echo "Waiting for Elastic Beanstalk Environment to be ready..."
    aws elasticbeanstalk wait environment-exists \
        --application-name "$EB_APP_NAME" \
        --environment-names "$EB_ENV_NAME" \
        --region $REGION
    
    sleep 30 # Additional wait for environment to stabilize
    
else
    echo "Elastic Beanstalk Environment already exists"
fi

# 4. Get Elastic Beanstalk URL
echo "Step 4: Getting Elastic Beanstalk URL..."
EB_URL=$(aws elasticbeanstalk describe-environments \
    --application-name "$EB_APP_NAME" \
    --environment-names "$EB_ENV_NAME" \
    --region $REGION \
    --query 'Environments[0].CNAME' \
    --output text)

echo "========================================"
echo "Deployment Completed Successfully!"
echo "========================================"
echo "Elastic Beanstalk URL: http://$EB_URL"
echo "Application Name: $EB_APP_NAME"
echo "Environment Name: $EB_ENV_NAME"
echo ""
echo "Your website is now hosted at: http://$EB_URL"
echo ""
echo "Note: Resources will continue running until manually deleted."
