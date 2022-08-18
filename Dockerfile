# Separate build image
FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app
COPY pyproject.toml .
COPY poetry.lock .
RUN pip install poetry \
 && poetry config virtualenvs.create false \
 && poetry install --no-dev --no-root --no-interaction --no-ansi \
COPY bot .

CMD ['poetry', 'run', 'bot-src']