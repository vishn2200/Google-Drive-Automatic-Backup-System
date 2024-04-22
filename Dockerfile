# Use Python base image
FROM python:3.9




# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir google-api-python-client google-auth-oauthlib google-auth-httplib2
# RUN pip install --no-cache-dir kubernetes
RUN apt-get update && apt-get install -y \
    python3-tk \
 && rm -rf /var/lib/apt/lists/*
RUN chmod -R 777 /app



# Expose any ports the app is expecting
EXPOSE 8080

# Run the application
CMD ["python", "backup_backend.py"]
# CMD ["bash", "-c", "sleep 10 && python backup_script.py"]

