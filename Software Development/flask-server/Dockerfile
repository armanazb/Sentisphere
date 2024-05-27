# Use the official Python image.
FROM python:3.9.17-slim

# Set environment variables to prevent Python from writing .pyc files to disk
# and to ensure output is sent straight to terminal (e.g. for Docker logs)
ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=production
ENV APP_HOME=/back-end

# Set the working directory
WORKDIR $APP_HOME

# Copy the application code to the working directory
COPY . .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Expose the port that the application will run on
EXPOSE 8080

ENV FLASK_APP=server.py

# Command to run the application
CMD ["gunicorn", "--bind", ":8080", "--workers", "1", "--threads", "8", "--timeout", "0", "app:app"]
