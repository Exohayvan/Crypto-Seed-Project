# Base image
FROM python:3.9.9-bullseye

# Set working directory
WORKDIR /app

# Copy requirements file
COPY ./requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Run the script
CMD [ "python3", "main.py" ]
