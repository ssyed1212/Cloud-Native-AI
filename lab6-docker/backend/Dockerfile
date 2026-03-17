FROM python:3.11-slim

WORKDIR /srv

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# backend constraints: derive python version/deps from lab4/pyproject.toml (requires-python >=3.10)
COPY lab4/pyproject.toml /srv/lab4/pyproject.toml

RUN python -m pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir \
      "fastapi>=0.100.0" \
      "uvicorn[standard]>=0.22.0" \
      "httpx>=0.24.0" \
      "python-dotenv>=1.0.0"

COPY lab4/ /srv/lab4/

WORKDIR /srv/lab4

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
