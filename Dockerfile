FROM python:3.8

# Set the working directory
WORKDIR /app


# Copy the requirements file into the container
COPY requirements.txt .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY . .

# Expose port 8080
EXPOSE 8080

# Command to run the application
RUN pip install -r requirements.txt
CMD ["python", "worker.py"]
