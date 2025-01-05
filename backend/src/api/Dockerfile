# Development stage
FROM python:3.12-bookworm AS development

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install pip requirements
COPY ./src/common/requirements.txt ./requirements-common.txt
RUN pip install -r ./requirements-common.txt

COPY ./src/api/requirements.txt ./requirements.txt
RUN pip install -r ./requirements.txt

COPY ./src/api/requirements-dev.txt ./requirements-dev.txt
RUN pip install -r ./requirements-dev.txt

EXPOSE 5678
EXPOSE 8000
EXPOSE 8265

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
RUN mkdir -p /app/shared_files && chown -R appuser /app/shared_files
USER appuser

ENV PYTHONPATH="${PYTHONPATH}:/app"

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]


# Production stage
FROM python:3.12-bookworm AS production

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY ./src/api/requirements.txt ./requirements.txt
RUN pip install -r ./requirements.txt

COPY ./src/api .

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
RUN mkdir -p /app/shared_files && chown -R appuser /app/shared_files
USER appuser

ENV PYTHONPATH="${PYTHONPATH}:/app"

EXPOSE 8000

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
