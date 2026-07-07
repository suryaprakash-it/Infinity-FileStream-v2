# Use a specific platform if you are on an ARM/M1/M2 Mac, otherwise this is fine
FROM python:3.11-slim

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies first (leverages Docker cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the port used by Render
EXPOSE 10000

# Start the application
CMD ["uvicorn", "web:app", "--host", "0.0.0.0", "--port", "10000"]
