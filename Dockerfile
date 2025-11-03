FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code and tests
COPY src/ ./src/
COPY tests/ ./tests/
COPY setup.py .

# Install the package
RUN pip install -e .

# Expose port (adjust as needed)
EXPOSE 80

# Run the application
CMD ["python", "src/main.py"]
