# Start with a Python base image. 'slim' is a smaller, more efficient version.
FROM python:3.10-slim

# Set the working directory inside the container. All subsequent commands will run from here.
WORKDIR /app

# Install system dependencies. 'build-essential' and 'gcc' are often needed for compiling Python packages.
# 'rm -rf /var/lib/apt/lists/*' cleans up the cache to keep the image size small.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc && \
    rm -rf /var/lib/apt/lists/*

# Copy the requirements file and install the Python dependencies.
# '--no-cache-dir' prevents pip from storing a cache, which also helps reduce image size.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application's files into the container.
COPY . .

# Set an environment variable. PYTHONUNBUFFERED=1 ensures that Python's output is not buffered,
# which is important for real-time logs in containerized applications.
ENV PYTHONUNBUFFERED=1

# Expose the port that Streamlit will use. This tells Docker to make this port accessible.
EXPOSE 8501

# The command to run when the container starts. This executes the Streamlit app.
CMD ["streamlit", "run", "Scripts/app.py"]
