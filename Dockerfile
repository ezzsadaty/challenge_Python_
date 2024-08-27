# Use an official Python runtime as a parent image
# FROM python:3.9-slim

# # Set environment variables to prevent Python from writing .pyc files and buffering stdout/stderr
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# # Set the working directory in the container
# WORKDIR /app

# # Copy the requirements file into the container
# COPY requirements.txt /app/

# # Install any necessary dependencies
# RUN pip install --no-cache-dir -r requirements.txt

# RUN pip install gunicorn

# # Copy the current directory contents into the container at /app
# COPY . /app/

# # Expose port 8000 for the Django app
# EXPOSE 8000

# # Start the Django server
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "tradvo_challenge.wsgi:application"]

# # Install system dependencies required by mysqlclient
# RUN apt-get update && apt-get install -y \
#     build-essential \
#     default-libmysqlclient-dev \
#     pkg-config \
#     && rm -rf /var/lib/apt/lists/*




# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables to prevent Python from writing .pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install any necessary dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# Install system dependencies required by mysqlclient
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user and switch to it
RUN useradd -m myuser
USER myuser

# Copy the current directory contents into the container at /app
COPY . /app/

# Collect static files (if applicable)
RUN python manage.py collectstatic --noinput

# Expose port 8000 for the Django app
EXPOSE 8000

# Health check to ensure the app is running
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s CMD curl -f http://localhost:8000/health/ || exit 1

# Start the Django server
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "tradvo_challenge.wsgi:application"]
