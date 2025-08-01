FROM python:3.12.11-bookworm

# Update system and install build dependencies
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends gcc && \
    rm -rf /var/lib/apt/lists/*

# Makes Bash the deafult shell
RUN ln -sf /bin/bash /bin/sh

# Install pipenv
RUN pip install pipenv

# Set working directory
WORKDIR /app

# Copy the Pipfile and Pipfile.lock
COPY ./todo_app/Pipfile .
COPY ./todo_app/Pipfile.lock .

# Create the requirements.tx file using pipenv
RUN pipenv requirements > requirements.txt

# Copy requirements file and install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY ./todo_app .

# Expose FastAPI default port
EXPOSE 8000

# Start FastAPI app (assuming main:app)
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
CMD ["tail", "-f", "/dev/null"]