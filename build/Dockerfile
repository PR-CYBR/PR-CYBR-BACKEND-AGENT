# syntax=docker/dockerfile:1
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_HOME=/app \
    AGENT_ENV=production \
    AGENT_PORT=8000

WORKDIR ${APP_HOME}

COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip \
    && if [ -s requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi

COPY . .

RUN pip install --no-cache-dir .

EXPOSE ${AGENT_PORT}

ENV PYTHONPATH=${APP_HOME}

ENTRYPOINT ["python", "-m", "src.main"]
