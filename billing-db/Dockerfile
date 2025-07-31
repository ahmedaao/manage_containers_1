FROM postgres:15

# Copy initialization script to Docker's entrypoint directory
COPY init.sql /docker-entrypoint-initdb.d/
