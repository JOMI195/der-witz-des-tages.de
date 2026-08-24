#!/bin/bash

# Check for at least 3 arguments
if [ "$#" -lt 3 ]; then
  echo "Usage: $0 <docker-compose-file> <env-file> <docker-compose-command> [<container-name>]"
  exit 1
fi

DOCKER_COMPOSE_FILE="$1"
ENV_FILE="$2"
DOCKER_COMPOSE_COMMAND="$3"
CONTAINER_NAME="${4:-all}"  # Default to 'all' if not provided

# Check if the Docker Compose file exists
if [ ! -f "$DOCKER_COMPOSE_FILE" ]; then
  echo "Error: Docker Compose file '$DOCKER_COMPOSE_FILE' not found!"
  exit 1
fi

# Check if the environment file exists
if [ ! -f "$ENV_FILE" ]; then
  echo "Error: Environment file '$ENV_FILE' not found!"
  exit 1
fi

# Generate the build version
BUILD_DATE=$(date -u +"%Y-%m-%d")
BUILD_UUID=$(uuidgen | tr '[:upper:]' '[:lower:]' | awk -F'-' '{print substr($1,1,8)}')
BUILD_VERSION="${BUILD_DATE}-${BUILD_UUID}"

export VITE_APP_BUILD_VERSION=$BUILD_VERSION

# Run the Docker Compose command
if [ "$CONTAINER_NAME" == "all" ]; then
  docker compose -f "$DOCKER_COMPOSE_FILE" --env-file "$ENV_FILE" $DOCKER_COMPOSE_COMMAND
else
  # Check if the specified container exists
  if ! docker compose -f "$DOCKER_COMPOSE_FILE" ps -q "$CONTAINER_NAME" > /dev/null; then
    echo "Error: Container '$CONTAINER_NAME' not found in the Docker Compose file!"
    exit 1
  fi

  # Run the command on the specified container
  docker compose -f "$DOCKER_COMPOSE_FILE" --env-file "$ENV_FILE" $DOCKER_COMPOSE_COMMAND "$CONTAINER_NAME"
fi

RESULT=$?

# A rebuilt nginx image ships an index.html without the tracker, so re-inject
# after every `up` of the full stack.
INJECT_SCRIPT="$(dirname "$0")/scripts/inject-umami-tracker.sh"
if [ "$RESULT" -eq 0 ] && [ "$CONTAINER_NAME" == "all" ] \
   && [ "$(echo "$DOCKER_COMPOSE_COMMAND" | awk '{print $1}')" == "up" ] \
   && grep -q "^  umami:" "$DOCKER_COMPOSE_FILE" \
   && grep -q "^  nginx:" "$DOCKER_COMPOSE_FILE"; then
  if [ -x "$INJECT_SCRIPT" ]; then
    "$INJECT_SCRIPT" "$DOCKER_COMPOSE_FILE" "$ENV_FILE" \
      || echo "Warning: umami tracker injection failed!"
  else
    echo "Warning: '$INJECT_SCRIPT' not found or not executable, skipping tracker injection!"
  fi
fi

exit $RESULT
