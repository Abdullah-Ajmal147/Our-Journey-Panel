#!/bin/bash
set -e

# Replace {YOUR_GIT_REOPO_URL} with your actual Git repository URL
#GIT_REPO_URL="https://github.com/Abdullah-Ajmal147/Our-Journey-Panel.git"

# If using Private Repo
#GIT_REPO_URL="https://<your_username>:<your_PAT>@github.com/codewithmuh/django-aws-ec2-autoscaling.git"

# Replace {YOUR_PROJECT_MAIN_DIR_NAME} with your actual project directory name
#PROJECT_MAIN_DIR_NAME="Our-Journey-Panel"

# Clone repository
#git clone "$GIT_REPO_URL" "/home/ubuntu/backend/$PROJECT_MAIN_DIR_NAME"

#cd "/home/ubuntu/backend/$PROJECT_MAIN_DIR_NAME"

# Make all .sh files executable
chmod +x scripts/*.sh

# Execute scripts for OS dependencies, Python dependencies, Gunicorn, Nginx, and starting the application
./scripts/instance_os_dependencies.sh
./scripts/python_dependencies.sh
./scripts/gunicorn.sh
./scripts/nginx.sh
./scripts/start_app.sh