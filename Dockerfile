# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt and install any needed packages specified in it
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Install Gunicorn (WSGI server)
RUN pip install gunicorn

# Expose port 5000 for the container
EXPOSE 5000

# Use Gunicorn to start the application
CMD ["gunicorn", "--config", "gunicorn_config.py", "app:app"]
