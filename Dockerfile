FROM python:3.9-slim

# Set up a working directory
WORKDIR /action

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your script
COPY check-notebooks.py .

RUN ls

# Define the entrypoint
ENTRYPOINT ["python", "/action/check-notebooks.py"]