# Base image
FROM python:3.9-slim-buster

# Set working directory
WORKDIR ./

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Run the script
CMD [ "python", "main.py" ]
