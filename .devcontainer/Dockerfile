FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN groupadd --gid 1000 vscode \
    && useradd --uid 1000 --gid vscode --shell /bin/bash --create-home vscode

# Set the working directory
WORKDIR /workspaces

# Create virtual environment
ENV VIRTUAL_ENV="/opt/venv"
RUN python -m venv $VIRTUAL_ENV \
    && . $VIRTUAL_ENV/bin/activate

# Activate virtual environment and add to PATH
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Copy requirements first for better caching
COPY requirements*.txt ./

# Install Python dependencies in virtual environment
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements-dev.txt

# Copy the rest of the application
COPY . .

# Change ownership of the workspace and virtual environment
RUN chown -R vscode:vscode /workspaces /opt/venv

# Switch to non-root user
USER vscode

# Set up Python path
ENV PYTHONPATH=/workspaces/pdf-stitcher/src
