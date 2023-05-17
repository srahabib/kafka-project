# Use a base image with Python and necessary dependencies
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the scraping script and any other necessary files to the container
COPY scraping_script.py requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the scraping script when the container starts
CMD ["python", "scraping_script.py"]
