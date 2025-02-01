FROM python:3.12-alpine3.20
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

RUN uv venv /opt/venv
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN uv pip install -r requirements.txt

COPY . /app

EXPOSE 8080

WORKDIR /app/src
CMD ["fastapi", "run", "--host", "0.0.0.0", "--port", "8080"]