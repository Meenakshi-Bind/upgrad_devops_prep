# Car Parking Management Application

A Django-based car parking management application with full CRUD operations, authentication, and AWS deployment.

## Features

- **User Authentication**: Registration, login, logout
- **Vehicle Management**: CRUD operations for vehicles
- **Parking Management**: Start/end parking sessions
- **Real-time Availability**: Track available parking spaces
- **Security**: OWASP compliance, SQL injection prevention, XSS protection
- **Deployment**: AWS Elastic Beanstalk with Terraform
- **CI/CD**: GitHub Actions pipeline with testing and security scanning

# Quick Start

# ### Local Development
# ```bash
# # Make setup script executable
# chmod +x scripts/setup.sh

# # Run setup
# ./scripts/setup.sh

# # Start the server
# source venv/bin/activate
# python manage.py runserver
