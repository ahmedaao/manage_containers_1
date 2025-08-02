# Base image
FROM alpine:3.18

# Copy the application into the container
WORKDIR /app
COPY app/ /app/

# Install Python3 & pip with base image debian
RUN apk add --no-cache python3 py3-pip && \
    pip3 install --break-system-packages -r requirements.txt

# API startup command
CMD ["python", "main.py"]
