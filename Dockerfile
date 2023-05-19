# Use the bitnami/spark:3 base image
FROM python:3.8-slim
# Set the working directory in the container

WORKDIR /app

# Set the user to root for permission changes
USER root

# Install additional dependencies for Kafka
RUN apt-get update && \
    apt-get install -y default-jre && \
    pip install confluent-kafka

# Copy the scraping script and any other necessary files to the container
COPY scraping_script.py requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Switch back to the non-root user
USER 1001

# Run the scraping script when the container starts
CMD ["python", "scraping_script.py"]

