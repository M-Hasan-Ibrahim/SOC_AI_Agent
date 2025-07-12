FROM python:3.11-slim

# working directory
WORKDIR /code

# Copy requirements.txt into the container
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your code into the container
COPY . .