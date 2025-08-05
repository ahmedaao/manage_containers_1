FROM rabbitmq:3-management

# Expose ports
EXPOSE 5672 15672

# Create data directory
RUN mkdir -p /var/lib/rabbitmq

# Set data directory as volume
VOLUME ["/var/lib/rabbitmq"]

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD rabbitmqctl status

# Start RabbitMQ
CMD ["rabbitmq-server"]