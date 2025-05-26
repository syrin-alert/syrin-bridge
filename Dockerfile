# Use a lightweight Alpine image of Python
FROM python:3.9-alpine

# Set the working directory inside the container
WORKDIR /app

# Copy requirements and install pika
COPY requirements.txt .

# Install Python dependencies (pika only) with no cache
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY ./app/ .

# Expose port 80
EXPOSE 80

# /home/vagrant/.local/share/tts/
# docker build -t didevlab/poc:syrin_bridge_queue-1.0.0 .

CMD ["python", "main.py"]