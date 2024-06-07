# Use the official NATS image as the base image
FROM nats:latest

# Set the working directory inside the container
WORKDIR /app

# Copy the configuration file into the container
COPY nats.conf /app/nats.conf

# Expose the NATS server port
EXPOSE 4222

# Start the NATS server
CMD ["nats-server", "-c", "/app/nats.conf"]