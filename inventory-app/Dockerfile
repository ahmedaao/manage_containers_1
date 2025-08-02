# Base image
FROM alpine:3.18

# Copy the application into the container
WORKDIR /app
COPY app/ /app/

# Install Python3 & pip with base image debian
# RUN apt-get update && \
#     apt-get install -y --no-install-recommends python3 python3-pip && \
#     apt-get clean && rm -rf /var/lib/apt/lists/* && \
#     pip3 install --break-system-packages -r requirements.txt

# Install Python3 & pip with base image alpine
RUN apk add --no-cache python3 py3-pip && \
    pip3 install --break-system-packages -r requirements.txt

# Expose the API port
EXPOSE 8080

# API startup command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
