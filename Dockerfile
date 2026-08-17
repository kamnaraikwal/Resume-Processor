FROM python:3.11-slim

RUN apt-get update && apt-get install -y poppler-utils && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt requirements.txt
COPY app/ /app/app/

RUN pip install -r requirements.txt

RUN mkdir -p /mnt/uploads

CMD ["uvicorn", "app.server:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]