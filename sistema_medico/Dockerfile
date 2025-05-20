FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Crear directorios necesarios y establecer permisos
RUN mkdir -p /app/staticfiles /app/media
RUN chmod -R 777 /app/staticfiles /app/media

# Create a non-root user to run the app but give it necessary permissions
RUN adduser --disabled-password --gecos '' appuser
RUN chown -R appuser:appuser /app

# Command to run the application
# This will be overridden by docker-compose command
USER appuser
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
