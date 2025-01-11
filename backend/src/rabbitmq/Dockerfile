FROM rabbitmq:3.13-management

# Copy our custom entrypoint script into the container
COPY ./src/rabbitmq/docker-entrypoint.sh /usr/local/bin/custom-entrypoint.sh
RUN chmod +x /usr/local/bin/custom-entrypoint.sh

# Override the original entrypoint with ours
ENTRYPOINT ["/usr/local/bin/custom-entrypoint.sh"]