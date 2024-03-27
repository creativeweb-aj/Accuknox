# Use the official Python 3.9.6 image.
# https://hub.docker.com/_/python
FROM python:3.9.6-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /code/

# Run the application on the port 8001
CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]
