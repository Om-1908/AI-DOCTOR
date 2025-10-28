FROM python:3.9-slim

WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Make sure the required directories exist
RUN mkdir -p /app/Models
RUN mkdir -p /app/Data.csv

# Expose the port the app runs on
EXPOSE 7860

# Command to run the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]