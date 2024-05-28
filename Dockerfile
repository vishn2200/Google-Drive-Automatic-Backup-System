# Use Python base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir google-api-python-client google-auth-oauthlib google-auth-httplib2

# Expose any ports the app is expecting
EXPOSE 8080

# Run the application
CMD ["python", "backup_backend.py"]

