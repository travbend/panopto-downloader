# ----- common_base -----
FROM python:3.12-bookworm AS common_base

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

WORKDIR /app

ENV PYTHONPATH="${PYTHONPATH}:/app"

# Install pip requirements
COPY ./src/common/requirements.txt ./requirements-common.txt
RUN pip install -r ./requirements-common.txt




# ----- api_base -----
FROM common_base AS api_base

COPY ./src/api/requirements.txt ./requirements.txt
RUN pip install -r ./requirements.txt

EXPOSE 8000

# ----- api_dev -----
FROM api_base AS api_dev

COPY ./src/api/requirements-dev.txt ./requirements-dev.txt
RUN pip install -r ./requirements-dev.txt

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
RUN mkdir -p /app/shared_files && chown -R appuser /app/shared_files
USER appuser

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# ----- api_prod -----
FROM api_base AS api_prod

COPY ./src/common ./common
COPY ./src/api ./api

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
RUN mkdir -p /app/shared_files && chown -R appuser /app/shared_files
USER appuser

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]




# ----- worker_base -----
FROM common_base AS worker_base

RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY ./src/worker/requirements.txt ./requirements.txt
RUN pip install -r ./requirements.txt

EXPOSE 5679

# ----- worker_dev -----
FROM worker_base AS worker_dev

COPY ./src/worker/requirements-dev.txt ./requirements-dev.txt
RUN pip install -r ./requirements-dev.txt

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
RUN mkdir -p /app/shared_files && chown -R appuser /app/shared_files

# Ensure appuser can execute ffmpeg
RUN chmod +x /usr/bin/ffmpeg && \
    chown appuser /usr/bin/ffmpeg

USER appuser


# ----- worker_prod -----
FROM worker_base AS worker_prod

COPY ./src/common ./common
COPY ./src/worker ./worker

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
RUN mkdir -p /app/shared_files && chown -R appuser /app/shared_files

# Ensure appuser can execute ffmpeg
RUN chmod +x /usr/bin/ffmpeg && \
    chown appuser /usr/bin/ffmpeg

USER appuser

# ----- worker_default_dev -----
FROM worker_dev AS worker_default_dev
CMD ["celery", "-A", "worker.main", "worker", "--loglevel=info"]

# ----- worker_beat_dev -----
    FROM worker_dev AS worker_beat_dev
CMD ["celery", "-A", "worker.main", "beat", "--loglevel=info"]

# ----- worker_default_prod -----
FROM worker_prod AS worker_default_prod
CMD ["celery", "-A", "worker.main", "worker", "--loglevel=info"]

# ----- worker_beat_prod -----
FROM worker_prod AS worker_beat_prod
CMD ["celery", "-A", "worker.main", "beat", "--loglevel=info"]


# ----- migration-dev -----
FROM common_base AS migration_dev

WORKDIR /app/common/data/sqlalchemy

CMD ["alembic", "upgrade", "head"]

# ----- migration-prod -----
FROM common_base AS migration_prod

COPY ./src/common ./common

WORKDIR /app/common/data/sqlalchemy

CMD ["alembic", "upgrade", "head"]