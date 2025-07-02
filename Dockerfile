# Dockerfile
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy code
COPY . .

# Install required system libs for cryptography
RUN apt-get update && \
    apt-get install -y build-essential libssl-dev libffi-dev python3-dev && \
    pip install --no-cache-dir -r requirements.txt

# Create uploads folder inside container
RUN mkdir -p uploads

# Expose Flask port
EXPOSE 5000

# Run the app
CMD ["python", "run.py"]
