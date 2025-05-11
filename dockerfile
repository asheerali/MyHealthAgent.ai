FROM python:3.13-slim

WORKDIR /app

# Copy requirements first for better layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Create a directory for .env file
RUN mkdir -p /app/config

# Expose the port Streamlit runs on
EXPOSE 8501

# Environment variables
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_ENABLE_CORS=false

# Command to run the application
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]