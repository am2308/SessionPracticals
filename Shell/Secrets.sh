#!/bin/bash

# Variables (replace with your values)
REPO=$1
ENV_NAME=$2  # Environment name (can be staging, testing, etc.)

# Declare an associative array for secrets (secret_name=secret_value)
declare -A SECRETS=(
  ["AWS_ACCOUNT_ID"]=$3
  ["AWS_OIDC_ROLE_ARN"]=$4
  ["AWS_REGION"]=$5
  ["CODEARTIFACT_DOMAIN"]=$6
  ["CODEARTIFACT_PYPI_REPOSITORY"]=$7
)

SECRETS=(
  "AWS_ACCOUNT_ID" "$3"
  "AWS_OIDC_ROLE_ARN" "$4"
  "AWS_REGION" "$5"
  "CODEARTIFACT_DOMAIN" "$6"
  "CODEARTIFACT_PYPI_REPOSITORY" "$7"
)
# Function to create the environment if it doesn't exist
create_environment() {
  echo "Creating GitHub environment: $ENV_NAME for repository: $REPO"
  gh api \
    --method PUT \
    -H "Accept: application/vnd.github.v3+json" \
    "/repos/$REPO/environments/$ENV_NAME" \
#    -f wait_timer="0" \
#    -F deployment_branch_policy="{\"protected_branches\": false, \"custom_branch_policies\": false}"

  if [[ $? -eq 0 ]]; then
    echo "Environment '$ENV_NAME' created or already exists."
  else
    echo "Failed to create environment. Exiting..."
    exit 1
  fi
}

# Check Bash version
BASH_VERSION_NUMBER=$(bash --version | grep version | cut -d '.' -f1 | cut -d ' ' -f4)

# Function to set secrets using GitHub CLI
set_secrets_associative() {
  for SECRET_NAME in "${!SECRETS[@]}"; do
    SECRET_VALUE="${SECRETS[$SECRET_NAME]}"
    
    if [[ -n "$SECRET_VALUE" ]]; then
      echo "Setting secret '$SECRET_NAME' for repository '$REPO'..."
      
      # Use GitHub CLI to set the secret
      gh secret set "$SECRET_NAME" \
        --body "$SECRET_VALUE" \
        --repo "$REPO"

      if [[ $? -eq 0 ]]; then
        echo "Secret '$SECRET_NAME' set successfully."
      else
        echo "Failed to set secret '$SECRET_NAME'."
        exit 1
      fi
    else
      echo "Secret '$SECRET_NAME' has an empty value. Skipping."
    fi
  done
}

# Function to set secrets using indexed array (for Bash < 4.0)
set_secrets_indexed() {
  for ((i=0; i<${#SECRETS[@]}; i+=2)); do
    SECRET_NAME="${SECRETS[i]}"
    SECRET_VALUE="${SECRETS[i+1]}"
    echo $SECRET_NAME
    echo $SECRET_VALUE
    if [[ -n "$SECRET_VALUE" ]]; then
      echo "Setting secret '$SECRET_NAME' for repository '$REPO'..."
      
      # Use GitHub CLI to set the secret
      gh secret set "$SECRET_NAME" \
        --body "$SECRET_VALUE" \
        --repo "$REPO"

      if [[ $? -eq 0 ]]; then
        echo "Secret '$SECRET_NAME' set successfully."
      else
        echo "Failed to set secret '$SECRET_NAME'."
        exit 1
      fi
    else
      echo "Secret '$SECRET_NAME' has an empty value. Skipping."
    fi
  done
}

# Check Bash version and run the appropriate function
if [[ "$BASH_VERSION_NUMBER" -ge 4 ]]; then
  echo "Bash version is 4.0 or newer. Using associative array."
  # Create the environment
  create_environment
  set_secrets_associative
else
  echo "Bash version is less than 4.0. Using indexed array."
  # Create the environment
  create_environment
  set_secrets_indexed
fi

echo "All secrets have been processed for repository '$REPO'."