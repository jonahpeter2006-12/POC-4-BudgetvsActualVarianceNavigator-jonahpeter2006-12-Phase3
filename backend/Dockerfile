FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY backend/requirements.txt ./requirements.txt

RUN pip install --no-cache-dir --default-timeout=300 --retries=10 -r requirements.txt

COPY backend/main.py ./backend/main.py
COPY backend/assistant.py ./backend/assistant.py
COPY backend/budget_data.csv ./backend/budget_data.csv
COPY data-science/outputs/ ./data-science/outputs/

EXPOSE 8000

CMD ["sh", "-c", "uvicorn backend.main:app --app-dir /app --host 0.0.0.0 --port ${PORT:-8000}"]
