# Development stage
FROM python:3.12-bookworm AS development

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pip requirements
COPY ./src/worker/requirements.txt ./requirements.txt
RUN pip install -r ./requirements.txt

COPY ./src/worker/requirements-dev.txt ./requirements-dev.txt
RUN pip install -r ./requirements-dev.txt

EXPOSE 5679

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
RUN mkdir -p /app/shared_files && chown -R appuser /app/shared_files

# Ensure appuser can execute ffmpeg
RUN chmod +x /usr/bin/ffmpeg && \
    chown appuser /usr/bin/ffmpeg

USER appuser

ENV PYTHONPATH="${PYTHONPATH}:/app"

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["celery", "-A", "main", "worker", "--concurrency=4", "--loglevel=info"]


# Development stage
FROM python:3.12-bookworm AS development-beat

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pip requirements
COPY ./src/worker/requirements.txt ./requirements.txt
RUN pip install -r ./requirements.txt

COPY ./src/worker/requirements-dev.txt ./requirements-dev.txt
RUN pip install -r ./requirements-dev.txt

EXPOSE 5679

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
RUN mkdir -p /app/shared_files && chown -R appuser /app/shared_files

# Ensure appuser can execute ffmpeg
RUN chmod +x /usr/bin/ffmpeg && \
    chown appuser /usr/bin/ffmpeg

USER appuser

ENV PYTHONPATH="${PYTHONPATH}:/app"

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["celery", "-A", "main", "beat", "--loglevel=info"]


# Production stage
FROM python:3.12-bookworm AS production

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pip requirements
COPY ./src/worker/requirements.txt ./requirements.txt
RUN pip install -r ./requirements.txt

COPY ./src/worker .

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
RUN mkdir -p /app/shared_files && chown -R appuser /app/shared_files

# Ensure appuser can execute ffmpeg
RUN chmod +x /usr/bin/ffmpeg && \
    chown appuser /usr/bin/ffmpeg

USER appuser

ENV PYTHONPATH="${PYTHONPATH}:/app"

CMD ["celery", "-A", "main", "worker", "--loglevel=info"]

