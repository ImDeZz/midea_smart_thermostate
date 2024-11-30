# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the requirements file into the container
COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code into the container
COPY . .

# Set an environment variable for the service account
ENV GOOGLE_APPLICATION_CREDENTIALS="/usr/src/app/service-account-key.json"

# Run the Python script
CMD ["python3", "main.py"]
