FROM python:3.8-slim
ENV PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on
WORKDIR /app
COPY . .
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction
