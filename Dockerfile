FROM python:3.10.9-slim

# Update apt-get and install Playwright dependencies
RUN apt-get update && apt-get install -y \
    wget \
    ffmpeg \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libatspi2.0-0 \
    libxcomposite1 \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any dependencies
RUN pip install -r requirements.txt

# Install Playwright and browser binaries
RUN pip install playwright && playwright install

# Install system dependencies required by Playwright to run browsers
RUN playwright install-deps

# Copy the content of the local src directory to the working directory
COPY . .

# Command to run on container start
CMD ["python3", "main.py"]
