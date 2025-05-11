# FROM python:3.10-slim

# WORKDIR /app

# # Install required system dependencies
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     locales \
#     && apt-get clean \
#     && rm -rf /var/lib/apt/lists/*

# # Optional: Set locale
# ENV LANG=en_US.UTF-8
# # Copy project files
# COPY ./ ./
# # Upgrade pip and install Streamlit
# RUN pip install --upgrade pip
# RUN pip install -r requirements.txt

# RUN pip install streamlit

# # Copy project files
# COPY ./ ./

# # Run Streamlit app
# CMD ["streamlit", "run", "main.py"]


# Use an official Python runtime as a parent image
FROM python:3.13-slim

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt ./requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Copy the current directory contents into the container at /app
COPY . /app

# Define the command to run the app using streamlit
ENTRYPOINT ["streamlit", "run"]
CMD ["app.py"]
