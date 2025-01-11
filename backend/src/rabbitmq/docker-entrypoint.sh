#!/usr/bin/env bash
set -e

export RABBITMQ_DEFAULT_PASS="$(cat /run/secrets/rabbitmq_password)"

# (Optional) Print info for debugging (comment out in production)
echo "RabbitMQ user: $RABBITMQ_DEFAULT_USER"
echo "RabbitMQ pass: [HIDDEN]"

# Chain to the original RabbitMQ entrypoint
exec /usr/local/bin/docker-entrypoint.sh rabbitmq-server
