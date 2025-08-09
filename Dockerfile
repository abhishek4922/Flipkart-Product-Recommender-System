FROM python:3.10-slim

# essential env variables

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# WORK DIRECTORY INSIDE THE DOCKER CONTAINER

WORKDIR /app

# installing the system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

#  copying ur all contents from local to app

COPY . .

# run setup.py

RUN pip install --no-cache-dir -e .

# expose ports
EXPOSE 5000


# RUN THE APP
CMD ["python","app.py"]


