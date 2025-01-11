FROM python:3.12-bookworm as development

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install pip requirements
COPY ./src/common/requirements.txt ./requirements-common.txt
RUN pip install -r ./requirements-common.txt

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

ENV PYTHONPATH="${PYTHONPATH}:/app"

WORKDIR /app/common/data/sqlalchemy

CMD ["alembic", "upgrade", "head"]
